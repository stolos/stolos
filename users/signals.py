from django.db.models.signals import pre_save
from django.dispatch import receiver

from users import models


@receiver(
    pre_save, sender=models.SSHPublicKey, dispatch_uid='update_ssh_public_key')
def update_ssh_public_key(sender, instance, **kwargs):
    instance.parse()
