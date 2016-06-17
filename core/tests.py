import os

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
