from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from users import models


@receiver(
    pre_save, sender=models.SSHPublicKey, dispatch_uid='update_ssh_public_key')
def update_ssh_public_key(sender, instance, **kwargs):
    instance.parse()

@receiver(post_delete, sender=Token, dispatch_uid='cert_cn_invalidation')
def invalidate_docker_cert(sender, instance, **kwargs):
    try:
        docker_cert = models.DockerCert.objects.get(token=instance.key)
    except models.DockerCert.DoesNotExist:
        pass
    docker_cert.delete()
