from rest_framework import filters, viewsets

from stolosd import permissions
from users import models, serializers


class SSHPublicKeyViewSet(viewsets.ModelViewSet):
    queryset = models.SSHPublicKey.objects.all()
    serializer_class = serializers.SSHPublicKeySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('md5', 'sha256', 'sha512')
