from __future__ import unicode_literals

import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models


class ProjectRoutingConfig(models.Model):
    """Configuration model for stolos projects"""
    project = models.OneToOneField(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='routing_config',
    )
    domain = models.CharField(max_length=256)
    config = JSONField()

    def get_domains_for_service_per_port(self, service_name, ports):
        """Returns the domain(s) that should be used for the given
        service and ports. Takes into account the config and the domain.

        Args:
            service_name: The name of the service to create the domain for.
            ports: A list of the ports used by the service.
        """
        if len(ports) == 0:
            return {}
        if self.config.get('subdomains') is True:
            return self._get_domains_for_service_with_subdomains(
                service_name, ports
            )
        else:
            return self._get_domains_for_service_no_subdomains(
                service_name, ports
            )

    def _get_domains_for_service_with_subdomains(self, service_name, ports):
        """Returns the domain(s) that should be used for the given
        service and ports. Uses subdomains.

        Args:
            service_name: The name of the service to create the domain for.
            ports: A list of the ports used by the service.
        """
        subdomain, _, domain = self.domain.partition('.')
        service_domains = {
            str(ports[0]): [
                '.'.join([service_name, self.domain]),
                '.'.join([
                    service_name, '{}-{}.{}'.format(subdomain, ports[0], domain)
                ])
            ]
        }
        for port in ports[1:]:
            service_domains[str(port)] = [
                '.'.join([
                    service_name, '{}-{}.{}'.format(subdomain, port, domain)
                ])
            ]
        if service_name == 'web':
            service_domains[str(ports[0])].append(self.domain)
            for port in ports:
                service_domains[str(port)].append(
                    '{}-{}.{}'.format(
                        subdomain, port, domain
                    )
                )
        return service_domains

    def _get_domains_for_service_no_subdomains(self, service_name, ports):
        """Returns the domain(s) that should be used for the given
        service and ports. Does not use subdomains.

        Args:
            service_name: The name of the service to create the domain for.
            ports: A list of the ports used by the service.
        """
        subdomain, _, domain = self.domain.partition('.')
        service_domains = {
            str(ports[0]): [
                '{}-{}.{}'.format(subdomain, service_name, domain),
                '{}-{}-{}.{}'.format(subdomain, service_name, ports[0], domain)
            ]
        }
        for port in ports[1:]:
            service_domains[str(port)] = [
                '{}-{}-{}.{}'.format(subdomain, service_name, port, domain)
            ]
        if service_name == 'web':
            service_domains[str(ports[0])].append(self.domain)
            for port in ports:
                service_domains[str(port)].append(
                    '{}-{}.{}'.format(subdomain, port, domain)
                )
        return service_domains

    def __unicode__(self):
        return '{} - {}'.format(self.project_id, self.domain)
