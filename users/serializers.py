from rest_framework import serializers

from users import models


class SSHPublicKeySerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CreateOnlyDefault(
            serializers.CurrentUserDefault()),
    )

    def update(self, instance, validated_data):
        validated_data.pop('public_key')
        return super(SSHPublicKeySerializer, self).update(
            instance, validated_data)

    class Meta:
        model = models.SSHPublicKey
        fields = ('uuid', 'name', 'public_key', 'md5', 'sha256', 'sha512',
                  'owner',)


class DockerCertSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DockerCert
        fields = ('cert_cn', )
