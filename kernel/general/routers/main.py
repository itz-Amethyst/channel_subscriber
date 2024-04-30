from rest_framework_nested import routers
from kernel.general.views.error import get_all_errors


router = routers.DefaultRouter()

router.register(r"errors", get_all_errors, basename="error-list")

urlpatterns = router.urls