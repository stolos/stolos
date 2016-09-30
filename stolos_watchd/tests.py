import os
import uuid

import mock
import requests

from django.test import TestCase
from django.test.utils import override_settings

from stolos_watchd import models
from stolos_watchd import watcher


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
        'stolos_watchd.models.ProjectRoutingConfig'
        '._get_domains_for_service_with_subdomains')
    def test_get_domains_for_service_with_subdomains(self, mck_get_domains):
        self.assertEquals(
            self.config.get_domains_for_service_per_port('some_service', [4242]),
            mck_get_domains.return_value)
        mck_get_domains.assert_called_once_with('some_service', [4242])

    @mock.patch(
        'stolos_watchd.models.ProjectRoutingConfig'
        '._get_domains_for_service_no_subdomains')
    def test_get_domains_for_service_no_subdomains(self, mck_get_domains):
        self.assertEquals(
            self.config_no_sub.get_domains_for_service_per_port('some_service', [4242]),
            mck_get_domains.return_value)
        mck_get_domains.assert_called_once_with('some_service', [4242])

    def test_get_domains_for_web_with_subdomains(self):
        self.assertEquals(
            self.config._get_domains_for_service_with_subdomains('web', [4242]),
            {
                '4242': [
                    'web.project.apps.lair.io',
                    'web.project-4242.apps.lair.io',
                    'project.apps.lair.io',
                    'project-4242.apps.lair.io'
                ]
            }
        )

    def test_get_domains_for_web_with_subdomains_multiple_ports(self):
        self.assertEquals(
            self.config._get_domains_for_service_with_subdomains(
                'web', [4242, 4243]),
            {
                '4242': [
                    'web.project.apps.lair.io',
                    'web.project-4242.apps.lair.io',
                    'project.apps.lair.io',
                    'project-4242.apps.lair.io'
                ],
                '4243': [
                    'web.project-4243.apps.lair.io',
                    'project-4243.apps.lair.io'
                ]
            }
        )

    def test_get_domains_for_web_no_subdomains(self):
        self.assertEquals(
            self.config._get_domains_for_service_no_subdomains('web', [4242]),
            {
                '4242': [
                    'project-web.apps.lair.io',
                    'project-web-4242.apps.lair.io',
                    'project.apps.lair.io',
                    'project-4242.apps.lair.io'
                ]
            }
        )

    def test_get_domains_for_web_no_subdomains_multiple_ports(self):
        self.assertEquals(
            self.config._get_domains_for_service_no_subdomains('web', [4242, 4243]),
            {
                '4242': [
                    'project-web.apps.lair.io',
                    'project-web-4242.apps.lair.io',
                    'project.apps.lair.io',
                    'project-4242.apps.lair.io'
                ],
                '4243': [
                    'project-web-4243.apps.lair.io',
                    'project-4243.apps.lair.io'
                ]
            }
        )

    def test_get_domains_for_svc_with_subdomains(self):
        self.assertEquals(
            self.config._get_domains_for_service_with_subdomains('svc', [4242]),
            {
                '4242': [
                    'svc.project.apps.lair.io',
                    'svc.project-4242.apps.lair.io'
                ]
            }
        )

    def test_get_domains_for_svc_with_subdomains_multiple_ports(self):
        self.assertEquals(
            self.config._get_domains_for_service_with_subdomains('svc', [4242, 4243]),
            {
                '4242': [
                    'svc.project.apps.lair.io',
                    'svc.project-4242.apps.lair.io'
                ],
                '4243': [
                    'svc.project-4243.apps.lair.io'
                ]
            }
        )

    def test_get_domains_for_svc_no_subdomains(self):
        self.assertEquals(
            self.config._get_domains_for_service_no_subdomains('svc', [4242]),
            {
                '4242': [
                    'project-svc.apps.lair.io',
                    'project-svc-4242.apps.lair.io'
                ]
            }
        )

    def test_get_domains_for_svc_no_subdomains_multiple_ports(self):
        self.assertEquals(
            self.config._get_domains_for_service_no_subdomains('svc', [4242, 4243]),
            {
                '4242': [
                    'project-svc.apps.lair.io',
                    'project-svc-4242.apps.lair.io'
                ],
                '4243': [
                    'project-svc-4243.apps.lair.io'
                ]
            }
        )

class WatcherTestSuite(TestCase):
    """Tests the logic of the watcher."""

    @classmethod
    def setUpClass(cls):
        super(WatcherTestSuite, cls).setUpClass()
        cls.routing_config = models.ProjectRoutingConfig(
            config={}, project_id=uuid.uuid4())
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

    @override_settings(DOCKER_HOST='unix:///var/run/stolos/docker.sock')
    def test_get_docker_client_unix(self):
        """Tests that a correct Docker client is returned"""
        self.assertEquals(watcher._get_docker_client().base_url,
                          'http+docker://localunixsocket')

    @override_settings(DOCKER_HOST='tcp://docker.example.com:4242',
                       DOCKER_CERT_PATH='/var/stolos/certs')
    @mock.patch('os.path.isfile', return_value=True)
    def test_get_docker_client(self, mck_isfile):
        """Tests that a correct Docker client is returned"""
        client = watcher._get_docker_client()
        self.assertEquals(client.base_url, 'https://docker.example.com:4242')
        self.assertEquals(client.verify, '/var/stolos/certs/ca.pem')
        self.assertEquals(client.cert, ('/var/stolos/certs/cert.pem',
                                        '/var/stolos/certs/key.pem'))

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

    @override_settings(DOCKER_IP='stolos-00.servers.lair.io')
    def test_get_container_url(self):
        self.assertEqual('stolos-00.servers.lair.io:32771',
                         watcher._get_container_url(self.mck_inspect_return, 32771))

    def test_get_container_ports_no_ports(self):
        container = self.mck_inspect_return.copy()
        container['NetworkSettings']['Ports'] = {}
        self.assertEqual(watcher._get_container_tcp_ports(container), [])

    @override_settings(DOCKER_IP='stolos-00.servers.lair.io')
    @mock.patch('stolos_watchd.watcher._should_route_container', return_value=True)
    @mock.patch('stolos_watchd.watcher._get_service', return_value='web')
    @mock.patch('stolos_watchd.watcher._get_container_tcp_ports',
                return_value=[4242])
    @mock.patch('stolos_watchd.models.ProjectRoutingConfig.get_domains_for_service_per_port',
                return_value={
                    '4242': [
                        'project-web.apps.lair.io',
                        'project-web-4242.apps.lair.io',
                        'project.apps.lair.io',
                        'project-4242.apps.lair.io',
                    ]
                })
    # Arguments are in reverse order
    @mock.patch('stolos_watchd.watcher.tasks.set_route.delay')
    @mock.patch('stolos_watchd.watcher.docker.Client.inspect_container')
    @mock.patch('stolos_watchd.watcher._get_routing_config')
    def test_process_event_start(self, mck_get_routing_config, mck_inspect,
                                 mck_task, *args):
        mck_get_routing_config.return_value = self.routing_config
        mck_inspect.return_value = self.mck_inspect_return
        watcher._process_event_start({})
        mck_task.assert_has_calls([
            mock.call('project-web.apps.lair.io',
                      'stolos-00.servers.lair.io:4242'),
            mock.call('project-web-4242.apps.lair.io',
                      'stolos-00.servers.lair.io:4242'),
            mock.call('project.apps.lair.io',
                      'stolos-00.servers.lair.io:4242'),
            mock.call('project-4242.apps.lair.io',
                      'stolos-00.servers.lair.io:4242'),
        ])

    @mock.patch('stolos_watchd.watcher._should_route_container', return_value=True)
    @mock.patch('stolos_watchd.watcher._get_service', return_value='web')
    @mock.patch('stolos_watchd.models.ProjectRoutingConfig.get_domains_for_service_per_port',
                return_value={
                    '4242': [
                        'project-web.apps.lair.io',
                        'project-web-4242.apps.lair.io',
                        'project.apps.lair.io',
                        'project-4242.apps.lair.io'
                    ]
                })
    @mock.patch('stolos_watchd.watcher._get_container_tcp_ports',
                return_value=[4242])
    # Arguments are in reverse order
    @mock.patch('stolos_watchd.watcher.tasks.unset_route.delay')
    @mock.patch('stolos_watchd.watcher.docker.Client.inspect_container')
    @mock.patch('stolos_watchd.watcher._get_routing_config')
    def test_process_event_die(self, mck_get_routing_config, mck_inspect,
                                 mck_task, *args):
        mck_get_routing_config.return_value = self.routing_config
        mck_inspect.return_value = self.mck_inspect_return
        watcher._process_event_die({})
        mck_task.assert_has_calls([
            mock.call('project-web.apps.lair.io'),
            mock.call('project-web-4242.apps.lair.io'),
            mock.call('project.apps.lair.io'),
            mock.call('project-4242.apps.lair.io')
        ])


    @mock.patch('stolos_watchd.watcher._process_event_die')
    @mock.patch('stolos_watchd.watcher._process_event_start')
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
