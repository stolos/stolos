from django.db import IntegrityError

from rest_framework.response import Response
from rest_framework.status import HTTP_409_CONFLICT
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    """
    Custom error handler, for returning a 409 response when the resources
    already exists.
    """
    response = drf_exception_handler(exc, context)
    if response:
        # Return the original response, if it was handled
        return response

    if type(exc) is IntegrityError and (
            'duplicate key value violates unique constraint' in exc.message):
        return Response({
            'detail': ['Resource already exists'],
        }, status=HTTP_409_CONFLICT)

    return None
