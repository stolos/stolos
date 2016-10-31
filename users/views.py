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
        cfssl_url = 'test'  # TODO: update to cfssl server endpoint
        certs = requests.post(cfssl_url, random_cn) # TODO: fix request
        token = token_serializer_class(token).data['auth_token']
        DockerCert.objects.create(token=token, cert_cn=random_cn)

        response_data = {
            'auth_token': token,
            'docker_key_pem': certs['docker_key_pem']
            'docker_cert_pem': certs['docker_cert_pem']
        }
        return Response(
            data=response_data,
            status=status.HTTP_200_OK,
        )
