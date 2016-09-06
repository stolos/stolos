from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from users import models


@admin.register(models.SSHPublicKey)
class SSHPublicKeyAdmin(GuardedModelAdmin):
    pass
