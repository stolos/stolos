from __future__ import unicode_literals

from uuid import uuid4

from django.contrib.postgres.fields import JSONField
from django.db import models


class ProjectRoutingConfig(models.Model):
    """Configuration model for sister projects"""
    project_id = models.UUIDField(default=uuid4, primary_key=True)
    user_id = models.CharField(max_length=30, blank=True)
    domain = models.CharField(max_length=256)
    config = JSONField()

    def get_domains_for_service(self, service_name):
        """Returns the domain(s) that should be used for the given
        service. Takes into account the config and the domain.

        Args:
            service_name: The name of the service to create the domain for.
        """
        return []


    def _get_domains_for_service_with_subdomains(self, service_name):
        """Returns the domain(s) that should be used for the given
        service. Uses subdomains.

        Args:
            service_name: The name of the service to create the domain for.
        """
        return []


    def _get_domains_for_service_no_subdomains(self, service_name):
        """Returns the domain(s) that should be used for the given
        service. Does not use subdomains.

        Args:
            service_name: The name of the service to create the domain for.
        """
        return []
