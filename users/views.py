import string

import requests
from django.utils import crypto
from djoser import utils
from djoser import serializers
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from users.models import DockerCert

class CustomLoginView(utils.ActionViewMixin, generics.GenericAPIView):
    """CustomLoginView to create docker certificates bound to the new token.
    """
    serializer_class = serializers.serializers_manager.get('login')
    permission_classes = (
        permissions.AllowAny,
    )

    def action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = serializers.serializers_manager.get('token')
        alphabet = string.ascii_lowercase + string.digits
        random_cn = crypto.get_random_string(32, alphabet)
        payload = {
            'request': {
                'CN': random_cn,
                'hosts': [''],
                'key': {
                    'algo': 'rsa',
                    'size': 2048
                },
                'names': [
                    {
                        'C': 'GR',
                        'O': 'SourceLair PC',
                        'ST': 'Athens'
                    }
                ],
            },
            'profile': 'client',
        }
        response = requests.post(
            'http://cfssl:8888/api/v1/cfssl/newcert', json=payload
        )
        DockerCert.objects.create(
            token=token, cert_cn=random_cn, owner=serializer.user)

        response_data = {
            'auth_token': token_serializer_class(token).data['auth_token'],
            'docker_key_pem': response.json()['result']['private_key'],
            'docker_cert_pem': response.json()['result']['certificate']
        }
        return Response(
            data=response_data,
            status=status.HTTP_200_OK,
        )
