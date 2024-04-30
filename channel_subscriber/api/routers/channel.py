from rest_framework_nested import routers
from channel_subscriber.api.views.channel import ChannelViewSet
from channel_subscriber.api.views.subscription import SubscriptionViewSet


router = routers.DefaultRouter()



router.register("channels", ChannelViewSet, basename="channels")
router.register("subscription", SubscriptionViewSet, basename="subscription")


urlpatterns = router.urls