from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.api.serializers.security.helper.cookie import delete_cookie
from core.api.serializers.security.jwt_logout import LogoutUserSerializer


class LogoutUserView(APIView):
    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post( self , request):
        serializer = self.serializer_class(data = request.data)

        serializer.is_valid(raise_exception = True)
        serializer.save()
        # can be set also in serializer
        if settings.USE_HTTP_ONLY_COOKIE:
            return delete_cookie(request = request)

        return Response(status = status.HTTP_204_NO_CONTENT)
