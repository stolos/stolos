import os
import uuid

import mock
import requests

from django.test import TestCase
from django.test.utils import override_settings

from core import models
from core import watcher


class ProjectRoutingConfigTestSuite(TestCase):
    """Tests the logic for the project routing config model."""

    @classmethod
    def setUpClass(cls):
        super(ProjectRoutingConfigTestSuite, cls).setUpClass()
        cls.config = models.ProjectRoutingConfig()
        cls.config.domain = 'project.apps.lair.io'
        cls.config.config = {'subdomains': True}
        cls.config_no_sub = models.ProjectRoutingConfig()
        cls.config_no_sub.domain = 'project.apps.lair.io'
        cls.config_no_sub.config = {'subdomains': False}

    @mock.patch(
        'core.models.ProjectRoutingConfig'
        '._get_domains_for_service_with_subdomains')
    def test_get_domains_for_service_with_subdomains(self, mck_get_domains):
        self.assertEquals(self.config.get_domains_for_service('some_service'),
                          mck_get_domains.return_value)
        mck_get_domains.assert_called_once_with('some_service')

    @mock.patch(
        'core.models.ProjectRoutingConfig'
        '._get_domains_for_service_no_subdomains')
    def test_get_domains_for_service_no_subdomains(self, mck_get_domains):
        self.assertEquals(
            self.config_no_sub.get_domains_for_service('some_service'),
            mck_get_domains.return_value)
        mck_get_domains.assert_called_once_with('some_service')

    def test_get_domains_for_web_with_subdomains(self):
        self.assertEquals(
            self.config._get_domains_for_service_with_subdomains('web'),
            ['project.apps.lair.io', 'web.project.apps.lair.io'])

    def test_get_domains_for_web_no_subdomains(self):
        self.assertEquals(
            self.config._get_domains_for_service_no_subdomains('web'),
            ['project.apps.lair.io', 'project-web.apps.lair.io'])

    def test_get_domains_for_svc_with_subdomains(self):
        self.assertEquals(
            self.config._get_domains_for_service_with_subdomains('svc'),
            ['svc.project.apps.lair.io'])

    def test_get_domains_for_svc_no_subdomains(self):
        self.assertEquals(
            self.config._get_domains_for_service_no_subdomains('svc'),
            ['project-svc.apps.lair.io'])


class WatcherTestSuite(TestCase):
    """Tests the logic of the watcher."""

    @classmethod
    def setUpClass(cls):
        super(WatcherTestSuite, cls).setUpClass()
        cls.routing_config = models.ProjectRoutingConfig(config={})
        cls.routing_config.save()
        project_id = cls.routing_config.project_id
        cls.mck_inspect_return = {
            'Config': {
                'Labels': {
                    'com.docker.compose.project': project_id,
                    'com.docker.compose.service': 'some-service',
                    'com.docker.compose.oneoff': 'False',
                    'com.docker.compose.container-number': '1',
                }
            },
            'NetworkSettings': {
                'Ports': {
                    '8000/tcp': [
                        {
                            'HostIp': '0.0.0.0',
                            'HostPort': '32771'
                        }
                    ]
                },
            }
        }

    @classmethod
    def tearDownClass(cls):
        super(WatcherTestSuite, cls).tearDownClass()
        cls.routing_config.delete()

    @override_settings(DOCKER_HOST='unix:///var/run/sister/docker.sock')
    def test_get_docker_client_unix(self):
        """Tests that a correct Docker client is returned"""
        self.assertEquals(watcher._get_docker_client().base_url,
                          'http+docker://localunixsocket')

    @override_settings(DOCKER_HOST='tcp://docker.example.com:4242',
                       DOCKER_CERT_PATH='/var/sister/certs')
    @mock.patch('os.path.isfile', return_value=True)
    def test_get_docker_client(self, mck_isfile):
        """Tests that a correct Docker client is returned"""
        client = watcher._get_docker_client()
        self.assertEquals(client.base_url, 'https://docker.example.com:4242')
        self.assertEquals(client.verify, '/var/sister/certs/ca.pem')
        self.assertEquals(client.cert, ('/var/sister/certs/cert.pem',
                                        '/var/sister/certs/key.pem'))

    def test_should_route_container(self):
        self.assertTrue(
            watcher._should_route_container(self.mck_inspect_return))
        for key in ['com.docker.compose.project',
                    'com.docker.compose.service',
                    'com.docker.compose.oneoff',
                    'com.docker.compose.container-number']:
            container = self.mck_inspect_return.copy()
            del container['Config']['Labels'][key]
            self.assertFalse(watcher._should_route_container(container))

    def test_should_route_container_oneoff(self):
        container = self.mck_inspect_return.copy()
        container['Config']['Labels'][
            'com.docker.compose.oneoff'] = 'True'
        self.assertFalse(watcher._should_route_container(container))

    def test_should_route_container_consecutive_container(self):
        container = self.mck_inspect_return.copy()
        container['Config']['Labels'][
            'com.docker.compose.container-number'] = '2'
        self.assertFalse(watcher._should_route_container(container))

    def test_get_routing_config(self):
        self.assertEqual(
            self.routing_config.project_id,
            watcher._get_routing_config(self.mck_inspect_return).project_id)

    def test_get_routing_config_not_exists(self):
        container = self.mck_inspect_return.copy()
        container['Config']['Labels'][
            'com.docker.compose.project'] = uuid.uuid4()
        self.assertIsNone(watcher._get_routing_config(container))

    def test_get_routing_config_invalid_id(self):
        container = self.mck_inspect_return.copy()
        container['Config']['Labels'][
            'com.docker.compose.project'] = 'invalid-uuid'
        self.assertIsNone(watcher._get_routing_config(container))

    def test_get_service(self):
        self.assertEqual('some-service',
                         watcher._get_service(self.mck_inspect_return))

    def test_get_container_url(self):
        self.assertEqual('localhost:32771',
                         watcher._get_container_url(self.mck_inspect_return))

    @override_settings(DOCKER_IP='sister-00.servers.lair.io')
    def test_get_container_url_dokcer_ip(self):
        self.assertEqual('sister-00.servers.lair.io:32771',
                         watcher._get_container_url(self.mck_inspect_return))

    def test_get_container_url_no_ports(self):
        container = self.mck_inspect_return.copy()
        container['NetworkSettings']['Ports'] = {}
        self.assertIsNone(watcher._get_container_url(container))

    @mock.patch('core.watcher._should_route_container', return_value=True)
    @mock.patch('core.watcher._get_service', return_value='web')
    @mock.patch('core.watcher._get_container_url',
                return_value='sister-00.servers.lair.io:4242')
    @mock.patch('core.models.ProjectRoutingConfig.get_domains_for_service',
                return_value=['project.apps.lair.io',
                              'project-web.apps.lair.io'])
    # Arguments are in reverse order
    @mock.patch('core.watcher.tasks.set_route.delay')
    @mock.patch('core.watcher.docker.Client.inspect_container')
    @mock.patch('core.watcher._get_routing_config')
    def test_process_event_start(self, mck_get_routing_config, mck_inspect,
                                 mck_task, *args):
        mck_get_routing_config.return_value = self.routing_config
        mck_inspect.return_value = self.mck_inspect_return
        watcher._process_event_start({})
        mck_task.assert_has_calls([
            mock.call('project.apps.lair.io',
                      'sister-00.servers.lair.io:4242'),
            mock.call('project-web.apps.lair.io',
                      'sister-00.servers.lair.io:4242')])

    @mock.patch('core.watcher._should_route_container', return_value=True)
    @mock.patch('core.watcher._get_service', return_value='web')
    @mock.patch('core.models.ProjectRoutingConfig.get_domains_for_service',
                return_value=['project.apps.lair.io',
                              'project-web.apps.lair.io'])
    # Arguments are in reverse order
    @mock.patch('core.watcher.tasks.unset_route.delay')
    @mock.patch('core.watcher.docker.Client.inspect_container')
    @mock.patch('core.watcher._get_routing_config')
    def test_process_event_die(self, mck_get_routing_config, mck_inspect,
                                 mck_task, *args):
        mck_get_routing_config.return_value = self.routing_config
        mck_inspect.return_value = self.mck_inspect_return
        watcher._process_event_die({})
        mck_task.assert_has_calls([
            mock.call('project.apps.lair.io'),
            mock.call('project-web.apps.lair.io')])


    @mock.patch('core.watcher._process_event_die')
    @mock.patch('core.watcher._process_event_start')
    def test_process_event(self, mck_start, mck_die):
        for status in ['attach', 'commit', 'copy', 'create', 'destroy',
                       'exec_create', 'exec_start', 'export', 'kill', 'oom',
                       'pause', 'rename', 'resize', 'restart',
                       'stop', 'top', 'unpause', 'update']:
            self.assertFalse(watcher.process_event(
                {'status': status, 'Type': 'container', 'id': 'some-id'}))
        event = {'status': 'start', 'Type': 'container', 'id': 'some-id'}
        self.assertTrue(watcher.process_event(event))
        mck_start.assert_called_once_with('some-id')
        event = {'status': 'die', 'Type': 'container', 'id': 'some-id'}
        self.assertTrue(watcher.process_event(event))
        mck_die.assert_called_once_with('some-id')
