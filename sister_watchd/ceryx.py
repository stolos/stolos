import os

import requests


class Client(object):
    """Creates a Client for managing routes for
    [Ceryx](https://github.com/sourcelair/ceryx)

    Args:
        host: The host that Ceryx API listens to.
        auth: The authentication that should be used, exactly like
            `requests`.
    """

    def __init__(self, host, auth=None):
        self.api_host = os.path.join(host, 'api/routes')
        self.auth = auth

    def set_route(self, source, target):
        """Sets route to point at target.

        Args:
            source: The source of the route.
            target: The target of the route.

        Returns:
            Ceryx response, in JSON format.
            Example:

            {
                'source': 'project.apps.lair.io',
                'target': "sister-00.servers.lair.io:45678"
            }

        Raises:
            requests.exceptions.HTTPError: The requests could not be fulfilled
                by the Ceryx API server.
            requests.exceptions.ConnectionError: Ceryx API host could not be
                reached.
            requests.exceptions.Timeout: The request timed out."""
        payload = {'source': source, 'target': target}
        resp = requests.post(self.api_host, json=payload, auth=self.auth)
        resp.raise_for_status()
        return resp.json()

    def unset_route(self, source):
        """Unsets a route, if it exists.

        Args:
            source: The source of the route.

        Returns:
            `True` if the request existed, `False` otherwise.

        Raises:
            requests.exceptions.HTTPError: The requests could not be fulfilled
                by the Ceryx API server. 404 responses will not raise an error.
            requests.exceptions.ConnectionError: Ceryx API host could not be
                reached.
            requests.exceptions.Timeout: The request timed out."""
        url = os.path.join(self.api_host, source)
        resp = requests.delete(url)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            if resp.status_code == 404:
                return False
            print resp.status_code
            raise
        return True
