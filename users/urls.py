from rest_framework import routers

from users import api


router = routers.SimpleRouter()
router.register(r'api/a0.1/keys', api.SSHPublicKeyViewSet)
urlpatterns = router.urls
