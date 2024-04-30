from django.urls import path
from core.api.views.security.logout import LogoutUserView
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("token/blacklist", TokenBlacklistView.as_view(), name='blacklist-token'),
]