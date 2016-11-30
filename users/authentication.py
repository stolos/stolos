from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

from users import models


class APITokenAuthentication(authentication.TokenAuthentication):
    model = models.APIToken
