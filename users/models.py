from __future__ import unicode_literals

import uuid

from django.db import models
from django.conf import settings
from sshpubkeys import SSHKey


class SSHPublicKey(models.Model):
    """
    Model storing the SSH public keys of a user. This also includes their
    MD5, SHA256 and SHA512 fingerprints.
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False)
    public_key = models.TextField(unique=True)
    md5 = models.CharField(unique=True, max_length=256, editable=False)
    sha256 = models.CharField(unique=True, max_length=256, editable=False)
    sha512 = models.CharField(unique=True, max_length=256, editable=False)
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('name', 'owner',)
        permissions = (
            ('view_sshpublickey', 'Can view public key'),
        )

    def parse(self):
        """
        Cleans the key from comments and options and pulates the MD5, SHA256
        and SHA512 sums.
        """
        ssh_key = SSHKey(
            self.public_key, parse_options=False, strict_mode=True)
        ssh_key.parse()
        # Tiny hack, to get the clean key
        self.public_key = ' '.join(ssh_key._split_key(ssh_key.keydata))
        self.md5 = ssh_key.hash_md5()
        self.sha256 = ssh_key.hash_sha256()
        self.sha512 = ssh_key.hash_sha512()
