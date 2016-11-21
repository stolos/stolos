from rest_framework import filters, viewsets

from users import models, serializers


class SSHPublicKeyViewSet(viewsets.ModelViewSet):
    queryset = models.SSHPublicKey.objects.all()
    serializer_class = serializers.SSHPublicKeySerializer
    filter_fields = ('md5', 'sha256', 'sha512')


class DockerCertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.DockerCert.objects.all()
    lookup_field = 'cert_cn'
    serializer_class = serializers.DockerCertSerializer
