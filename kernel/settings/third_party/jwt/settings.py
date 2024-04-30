from datetime import timedelta
from kernel.settings.development.configs import USE_HTTP_ONLY_COOKIE

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=5),
}

# Check if USE_HTTP_ONLY_COOKIE is True
# if USE_HTTP_ONLY_COOKIE:
#     # Update SIMPLE_JWT dictionary with TOKEN_OBTAIN_SERIALIZER key
#     SIMPLE_JWT["TOKEN_OBTAIN_SERIALIZER"] = "core.api.serializers.security.jwt_cookie.CustomJWTHTTPSerializer"
#     print(SIMPLE_JWT)