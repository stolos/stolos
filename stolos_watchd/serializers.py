from rest_framework import serializers

from stolos_watchd import models


class ProjectRoutingConfigSerializer(serializers.ModelSerializer):
    config = serializers.JSONField()

    class Meta:
        model = models.ProjectRoutingConfig
        fields = ('project', 'domain', 'config')
        read_only_fields = ('project',)
