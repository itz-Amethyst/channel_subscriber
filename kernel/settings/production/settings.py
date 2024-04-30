import os

from kernel.settings.base.settings import *

from kernel.settings.config.setup import env, BASE_DIR_FOR_UPLOAD

public_root = os.path.join(BASE_DIR_FOR_UPLOAD, 'public')

MEDIA_ROOT = os.path.join(public_root, 'media')
MEDIA_URL = env.str('MEDIA_URL', default='media/')

STATIC_ROOT = os.path.join(public_root, 'static')
STATIC_URL = env.str('STATIC_URL', default='static/')

DEBUG = False

ALLOWED_HOSTS +=  [host.strip() for host in env("ALLOWED_HOSTS").split(',')]

# for host in env("ALLOWED_HOSTS").split(","):
#     ALLOWED_HOSTS.append(host)

INSTALLED_APPS += [
    'djoser',

]

MIDDLEWARE += [
    'kernel.middleware.security_header_middleware.SecurityHeadersMiddleware'
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

REST_FRAMEWORK.update({
    "DEFAULT_RENDERER_CLASSES": ['rest_framework.renderers.JSONRenderer'],

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        # General
        'anon': '100/day',
        'user': '1000/day',
        # Only apply on class_rooms view
        'class_rooms': '150/day',
    }
})