import djoser.urls.jwt
from django.contrib import admin
from django.urls import path , include , re_path
from drf_spectacular.views import SpectacularAPIView , SpectacularSwaggerView
from core.api.views.security.cookie import Custom

# Assuming djoser.urls.jwt.urlpatterns is a list
jwt_urlpatterns = djoser.urls.jwt.urlpatterns

# Pop the first URL pattern if it exists which is create
if jwt_urlpatterns:
    jwt_urlpatterns.pop(0)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include(jwt_urlpatterns)),
    path("account/" , include("core.api.routers.jwt")) ,
    # path("auth/jwt/create/", Custom.as_view()),
    re_path(r"^auth/jwt/create/?", Custom.as_view(), name="jwt-create"),
    path("channel/" , include("channel_subscriber.api.routers.school")),
    path("general/", include("kernel.general.routers.main")),


    # ! Docs
    path('api/schema/' , SpectacularAPIView.as_view() , name = 'schema') ,
    path('api/docs/' , SpectacularSwaggerView.as_view(url_name = 'schema') , name = 'swagger-ui') ,
]
