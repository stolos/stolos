# -*- coding: utf-8 -*-

import os

from .context import sister_watchd

import mock
import requests
import unittest


class CeryxClientTestSuite(unittest.TestCase):
    """Tests for the Ceryx client."""

    @classmethod
    def setUpClass(cls):
        cls.mck_requests = mock.patch('sister_watchd.ceryx.requests')
        cls.api_host = 'https://ceryx.sister.io'
        cls.routes_url = os.path.join(cls.api_host, 'api/routes')
        cls.route_details_url = os.path.join(cls.routes_url, '{}')
        cls.source = 'project.apps.lair.io'
        cls.target = 'sister-00.servers.lair.io:55842'

    def setUp(self):
        self.client = sister_watchd.ceryx.Client(self.api_host)
        self.mck_requests_patch = self.mck_requests.start()

    def tearDown(self):
        self.mck_requests.stop()

    def test_set_route(self):
        self.client.set_route(self.source, self.target)
        self.mck_requests_patch.post.assert_called_once_with(
            self.routes_url,
            json={'source': self.source, 'target': self.target},
            auth=None)

    def test_unset_route(self):
        assert self.client.unset_route(self.source)
        self.mck_requests_patch.delete.assert_called_once_with(
            self.route_details_url.format(self.source, auth=None))

    def test_unset_route_404(self):
        response = mock.Mock()
        response.status_code = 404
        err = requests.exceptions.HTTPError
        response.raise_for_status.side_effect = err
        self.mck_requests_patch.delete.return_value = response
        # Revert exceptions to normal, in order to be able to catch it
        self.mck_requests_patch.exceptions = requests.exceptions
        assert self.client.unset_route(self.source) is False
        self.mck_requests_patch.delete.assert_called_once_with(
            self.route_details_url.format(self.source, auth=None))


if __name__ == '__main__':
    unittest.main()
