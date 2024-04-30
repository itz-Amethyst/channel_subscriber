from rest_framework_nested import routers
from core.api.views.profile import ProfileViewSet

router = routers.DefaultRouter()


router.register("profile", ProfileViewSet, basename="profiles")

urlpatterns = router.urls