from rest_framework.exceptions import APIException


class CFSSLError(APIException):
    status_code = 503
    default_detail = 'Could not create Docker certificate.'
    default_code = 'docker_certificate_service_unavailable'
