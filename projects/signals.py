from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm

from projects import models


@receiver(pre_save, sender=models.Stack, dispatch_uid='update_stack_slug')
def update_stack_slug(sender, instance, **kwargs):
    instance.slug = '{}/{}'.format(instance.owner, instance.name)


@receiver(pre_save, sender=models.Project, dispatch_uid='add_project_server')
def add_project_server(sender, instance, **kwargs):
    try:
        instance.server
    except models.Server.DoesNotExist:
        instance.server = models.Server.objects.order_by('?').first()


@receiver(post_save, sender=models.Project,
          dispatch_uid='add_permissions_to_project_owner')
def add_permissions_to_project_owner(sender, instance, **kwargs):
    if 'created' not in kwargs or not kwargs['created']:
        return
    for perm in ['view', 'change', 'delete']:
        perm_kwargs = {
            'app_label': sender._meta.app_label,
            'model_name': sender._meta.model_name,
            'perm': perm,
        }
        permission = '%(app_label)s.%(perm)s_%(model_name)s' % perm_kwargs
        assign_perm(permission, instance.owner, instance)


@receiver(post_save, sender=models.Project,
          dispatch_uid='add_permissions_to_stack_owner')
def add_permissions_to_stack_owner(sender, instance, **kwargs):
    if 'created' not in kwargs or not kwargs['created']:
        return
    perm_kwargs = {
        'app_label': sender._meta.app_label,
        'model_name': sender._meta.model_name,
        'perm': 'create_project',
    }
    permission = '%(app_label)s.%(perm)s_%(model_name)s' % perm_kwargs
    assign_perm(permission, instance.owner, instance)
