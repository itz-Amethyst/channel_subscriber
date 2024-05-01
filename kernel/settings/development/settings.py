import os

from kernel.settings.base.settings import *
from kernel.settings.config.setup import env, BASE_DIR_FOR_UPLOAD



public_root = os.path.join(BASE_DIR_FOR_UPLOAD, 'public')

MEDIA_ROOT = os.path.join(public_root, 'media')
MEDIA_URL = env.str('MEDIA_URL', default='media/')

STATIC_ROOT = os.path.join(public_root, 'static')
STATIC_URL = env.str('STATIC_URL', default='static/')

DEBUG = True

ALLOWED_HOSTS +=  [host.strip() for host in env("ALLOWED_HOSTS").split(',')]

# for host in env("ALLOWED_HOSTS").split(","):
#     ALLOWED_HOSTS.append(host)


INSTALLED_APPS += [
    "djoser" ,
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "corsheaders",
    "django_celery_results",
    "django_celery_beat",
]

MIDDLEWARE += [
    'kernel.middleware.security_header_middleware.SecurityHeadersMiddleware',
    'kernel.middleware.sanitize_text_middleware.SanitizeTextFieldMiddleware'
]

# postgresql
# ====================
DATABASES = {
    'default': {
        'ENGINE': env('DATABASE_ENGINE'),
        'NAME': env('DATABASE_NAME'),
        # 'HOST': env('DATABASE_HOST'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASS'),
        # 'PORT': env('DATABASE_PORT')
    }
}
