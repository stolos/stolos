import logging

from guardian.shortcuts import get_objects_for_user
from rest_framework import serializers

from projects import models
from stolos_watchd.models import ProjectRoutingConfig
from stolos_watchd.serializers import ProjectRoutingConfigSerializer


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Server


class StackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stack


class ProjectSerializer(serializers.ModelSerializer):
    routing_config = ProjectRoutingConfigSerializer(many=False)
    server = ServerSerializer(many=False, read_only=True)
    set_stack = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=models.Stack.objects.all(),
        write_only=True,
    )
    stack = StackSerializer(many=False, read_only=True)
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault()),
    )

    def __init__(self, *args, **kwargs):
        super(ProjectSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['stack'].queryset = get_objects_for_user(
                self.context['request'].user, ['view_stack'], models.Stack)

    class Meta:
        model = models.Project
        fields = ('uuid', 'stack', 'set_stack', 'server', 'owner', 'created',
                  'last_update', 'routing_config')
        read_only_fields = ('uuid', 'server', 'created', 'last_update')

    def create(self, validated_data):
        routing_config = validated_data.pop('routing_config')
        validated_data['stack'] = validated_data.pop('set_stack')
        project = models.Project(**validated_data)
        project.save()
        ProjectRoutingConfig(project=project, **routing_config).save()
        return project
