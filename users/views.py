import string

import requests
from django.contrib.auth import user_logged_in
from django.utils import crypto
from djoser import utils
from djoser import serializers
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from users.exceptions import CFSSLError
from users.models import DockerCert, APIToken


class CustomLoginView(utils.ActionViewMixin, generics.GenericAPIView):
    """CustomLoginView to create docker certificates bound to the new token.
    """
    serializer_class = serializers.serializers_manager.get('login')
    permission_classes = (
        permissions.AllowAny,
    )

    def _login_user(self, request, user):
        token = APIToken.objects.create(
            user=user, user_agent=request.META.get('HTTP_USER_AGENT')[:255])
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        return token

    def _create_docker_cert(self, token):
        random_cn = crypto.get_random_string(32)
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
        try:
            response = requests.post(
                'http://cfssl:8888/api/v1/cfssl/newcert', json=payload
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            raise CFSSLError(err.message)
        DockerCert.objects.create(
            token=token, cert_cn=random_cn, owner=token.user)
        result = response.json()['result']
        return result['certificate'], result['private_key']

    def action(self, serializer):
        token = self._login_user(self.request, serializer.user)
        token_serializer_class = serializers.serializers_manager.get('token')
        certificate, private_key = self._create_docker_cert(token)
        response_data = {
            'auth_token': token_serializer_class(token).data['auth_token'],
            'docker_key_pem': private_key,
            'docker_cert_pem': certificate,
        }
        return Response(data=response_data, status=status.HTTP_200_OK)
