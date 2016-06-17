import os

import docker

from django.conf import settings


def _get_docker_client():
    """Gets a Docker client, using the configuration defined in settings.py"""
    tls_config = None
    if settings.DOCKER_CERT_PATH:
        tls_config = docker.tls.TLSConfig(
            client_cert=(
                os.path.join(settings.DOCKER_CERT_PATH, 'cert.pem'),
                os.path.join(settings.DOCKER_CERT_PATH, 'key.pem')),
            verify=os.path.join(settings.DOCKER_CERT_PATH, 'ca.pem'))
    return docker.Client(base_url=settings.DOCKER_HOST, tls=tls_config)
