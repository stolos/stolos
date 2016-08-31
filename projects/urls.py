from rest_framework import routers

from projects import api


router = routers.SimpleRouter()
router.register(r'api/a0.1/projects', api.ProjectViewSet)
router.register(r'api/a0.1/stacks', api.StackViewSet)
urlpatterns = router.urls
