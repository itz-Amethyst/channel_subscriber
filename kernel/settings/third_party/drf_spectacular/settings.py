from kernel.settings.third_party.rest_framework.settings import REST_FRAMEWORK

SPECTACULAR_SETTINGS = {
    'TITLE': 'Channel Subscriber API',
    'DESCRIPTION': 'This is a Channel Subscriber official API documentation.',
    'VERSION': '1.0.0',
    # 'SERVE_INCLUDE_SCHEMA': False
}

REST_FRAMEWORK_CUSTOM_SETTINGS = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # to enable standardize
    # "DEFAULT_SCHEMA_CLASS": "drf_standardized_errors.openapi.AutoSchema"
}

REST_FRAMEWORK.update(REST_FRAMEWORK_CUSTOM_SETTINGS)