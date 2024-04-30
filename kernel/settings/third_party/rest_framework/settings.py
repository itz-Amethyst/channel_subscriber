from kernel.settings.base.settings import REST_FRAMEWORK
REST_FRAMEWORK.update({
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    #! Not sure
    "EXCEPTION_HANDLER": 'kernel.errors.custom_error.custom_exception_handler',
})