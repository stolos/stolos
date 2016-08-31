from rest_framework import filters, viewsets

from projects import models, serializers


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    filter_backends = (filters.DjangoObjectPermissionsFilter,)


class StackViewSet(viewsets.ModelViewSet):
    queryset = models.Stack.objects.all()
    serializer_class = serializers.StackSerializer
    filter_backends = (filters.DjangoObjectPermissionsFilter,)
