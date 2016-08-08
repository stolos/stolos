from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from projects import models


@admin.register(models.Stack)
class StackAdmin(GuardedModelAdmin):
    pass


@admin.register(models.Project)
class ProjectAdmin(GuardedModelAdmin):
    pass


@admin.register(models.Server)
class ServerAdmin(GuardedModelAdmin):
    pass
