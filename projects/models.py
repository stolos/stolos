from __future__ import unicode_literals

import uuid

import django.contrib.auth.models

from django.db import models
from django.conf import settings


class Server(models.Model):
    """
    Servers contain the needed information for connecting and syncing files with
    a Stolos server.

    :param docker_ca_pem: ca.pem to use for connecting to Docker
    :param host: the server IP or hostname to use when connecting
    :param created: the date this stack was created
    :param last_update: the date this stack was last updated

    :type docker_ca_pem: string
    :type host: string
    :type created: string
    :type last_update: string
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False)
    docker_ca_pem = models.TextField()
    host = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.host

    def __str__(self):
        return unicode(self)


class Stack(models.Model):
    """
    Stacks are the basic building blocks of Stolos projects. Stacks contain the
    needed Docker Compose file that should stay the same for all projects
    created by this Stack. Also, by updating the Docker Compose file of a Stack,
    all the projects created by it should be updated automatically.

    :param docker_compose_file: Docker compose file
    :param owner: the company owning this stack
    :param slug: the slug of the stack, automatically compiled from owner/name
    :param description: a short stack description
    :param created: the date this stack was created
    :param last_update: the date this stack was last updated

    :type docker_compose_file: string
    :type owner: django.contrib.auth.models.Group
    :type slug: string
    :type description: string
    :type created: datetime
    :type last_update: datetime
    """
    name = models.CharField(max_length=32)
    docker_compose_file = models.TextField()
    owner = models.ForeignKey(
        django.contrib.auth.models.Group,
        on_delete=models.CASCADE,
    )
    slug = models.CharField(max_length=64, editable=False)
    description = models.CharField(max_length=140, editable=False, default='')
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('owner', 'name')
        permissions = (
            ('view_stack', 'Can view this stack'),
        )

    def __unicode__(self):
        return self.slug

    def __str__(self):
        return unicode(self)


class Project(models.Model):
    """
    Projects are created from stacks and represent the unit that developers work
    on. They have an one-to-one relationship with routing configs - every
    project needs to have exactly one routing config associated with it.

    :param uuid: the project's unique identifier
    :param stack: the stack that this project relates to
    :param server: the stolos server this project was assigned
    :param owner: the user owning this project
    :param created: the date this stack was created
    :param last_update: the date this stack was last updated

    :type uuid: uuid
    :type stack: projects.models.Stack
    :type owner: django.contrib.auth.models.User
    :type created: datetime
    :type last_update: datetime
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False)
    stack = models.ForeignKey('projects.Stack', on_delete=models.SET_NULL, null=True, blank=True)
    server = models.ForeignKey('projects.Server',
                               on_delete=models.PROTECT,
                               editable=False,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ('view_project', 'Can view this project'),
        )

    def __unicode__(self):
        return '{} [{} - {}]'.format(self.uuid, self.stack, self.owner)

    def __str__(self):
        return unicode(self)
