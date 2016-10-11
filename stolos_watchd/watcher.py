import os
import logging

import docker

from django.conf import settings
from django.core.cache import cache

from stolos_watchd import models
from stolos_watchd import tasks


LOGGER = logging.getLogger('django')


def _get_docker_client():
    """Gets a Docker client, using the configuration defined in settings.py"""
    tls_config = None
    if settings.DOCKER_CERT_PATH:
        tls_config = docker.tls.TLSConfig(
            client_cert=(
                os.path.join(settings.DOCKER_CERT_PATH, 'cert.pem'),
                os.path.join(settings.DOCKER_CERT_PATH, 'key.pem')),
            verify=os.path.join(settings.DOCKER_CERT_PATH, 'ca.pem'),
            assert_hostname=False)
    return docker.Client(base_url=settings.DOCKER_HOST, tls=tls_config)


def _should_route_container(container):
    """Returns True, if and only if the given container contains the needed
    labels:
    * `com.docker.compose.project`
    * `com.docker.compose.service`
    * `com.docker.compose.oneoff`
    * `com.docker.compose.container-number`
    """
    labels = container.get('Config', {}).get('Labels', {})
    for label in ['com.docker.compose.project',
                  'com.docker.compose.service',
                  'com.docker.compose.oneoff',
                  'com.docker.compose.container-number']:
        if label not in labels:
            return False
    if labels['com.docker.compose.oneoff'] != 'False':
        return False
    if labels['com.docker.compose.container-number'] != '1':
        return False
    return True


def _get_routing_config(container):
    """Returns the project routing config assosiated with the given container
    using the `com.docker.compose.project` label or None"""
    project_id = container['Config']['Labels']['com.docker.compose.project']
    try:
        return models.ProjectRoutingConfig.objects.get(project_id=project_id)
    except (models.ProjectRoutingConfig.DoesNotExist, ValueError):
        return None


def _get_service(container):
    """Returns the project service assosiated with the given container using
    the `com.docker.compose.service` label or None"""
    return container['Config']['Labels']['com.docker.compose.service']


def _get_container_tcp_ports(container):
    """Returns the container's tcp ports, if any, or an empty list
    """
    container_ports = container['NetworkSettings']['Ports']
    if container_ports is None:
        return []
    ports = []
    for port_key in container_ports:
        if 'tcp' in port_key and container_ports[port_key] is not None:
            ports.append(container_ports[port_key][0]['HostPort'])
    return ports


def _get_container_url(container, port):
    """Returns the container's URL, using the `DOCKER_IP` setting defined in
    `settings.py` and the given port
    """
    return '{}:{}'.format(settings.DOCKER_IP, port)


def _process_event_start(event):
    """Processes a container start, setting the correct routing if needed."""
    container = _get_docker_client().inspect_container(event)
    if not _should_route_container(container):
        return
    project_routing_config = _get_routing_config(container)
    if project_routing_config is None:
        return
    service = _get_service(container)
    if service is None:
        return
    ports = _get_container_tcp_ports(container)
    domains = project_routing_config.get_domains_for_service_per_port(
        service, ports
    )
    for port in ports:
        for domain in domains.get(str(port), []):
            tasks.set_route.delay(domain, _get_container_url(container, port))


def _process_event_die(event):
    """Processes a container die, unsetting its route if existed."""
    container = _get_docker_client().inspect_container(event)
    if not _should_route_container(container):
        return
    project_routing_config = _get_routing_config(container)
    if project_routing_config is None:
        return
    service = _get_service(container)
    if service is None:
        return
    ports = _get_container_tcp_ports(container)
    domains = project_routing_config.get_domains_for_service_per_port(
        service, ports
    )
    for port in ports:
        for domain in domains.get(str(port), []):
            tasks.unset_route.delay(domain)


def process_event(event):
    """Processes events from Docker. Dispatches each even to the correct
    function."""
    event_type = event['Type']
    if event_type != 'container':
        LOGGER.debug('Discarding event of type %s', event_type)
        return
    status = event['status']
    container_id = event['id']
    LOGGER.info('Processing event %s -> %s', container_id, status)
    if status == 'start':
        _process_event_start(container_id)
        return True
    if status == 'die':
        _process_event_die(container_id)
        return True
    LOGGER.debug('Discarding event %s -> %s', container_id, status)
    return False


def watch():
    """Starts watching the Docker daemon for events and dispatches them."""
    since = cache.get('watcher:since')
    client = _get_docker_client()
    for event in client.events(decode=True, since=since):
        process_event(event)
        cache.set('watcher:since', event['time'])
