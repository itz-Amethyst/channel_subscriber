from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
       
        if type(request.user) == AnonymousUser:
            raise AuthenticationFailed(detail="Authentication credentials were not provided.")
        return bool(request.user and request.user.is_superuser)
