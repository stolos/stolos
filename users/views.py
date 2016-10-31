import requests
from django.utils import crypto
from djoser import utils
from djoser.views import LoginView
from users.models import DockerCert

class CustomLoginView(LoginView):
    """CustomLoginView to create docker certificates bound to the new token.
    """

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = serializers.serializers_manager.get('token')
        alphabet = string.ascii_lowercase + string.digits
        random_cn = crypto.get_random_string(32, alphabet)
        payload = {
            "CN": random_cn,
            "hosts": [""],
            "names": {
                "C": "GR",
                "O": "SourceLair PC",
                "ST": "Athens"
            },
            "profile": random_cn
        }
        response = requests.post(
            'cfssl/api/v1/cfssl/newcert', payload
        )
        token = token_serializer_class(token).data['auth_token']
        DockerCert.objects.create(token=token, cert_cn=random_cn)

        response_data = {
            'auth_token': token,
            'docker_key_pem': response['result']['private_key'],
            'docker_cert_pem': response['result']['certificate']
        }
        return Response(
            data=response_data,
            status=status.HTTP_200_OK,
        )
