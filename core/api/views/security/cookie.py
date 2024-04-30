from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from core.api.serializers.security.helper.cookie import create_cookie

class Custom(TokenObtainPairView):

    serializer_class = TokenObtainPairSerializer
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)

        if settings.USE_HTTP_ONLY_COOKIE:
            create_cookie(response = response, token = response.data['access'])

        return response