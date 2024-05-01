DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'auth/users/reset_password_confirm/{uid}/{token}',
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
    'EXCLUDE_FROM_API': ['users'],

    "PERMISSIONS": {
        'user_create': ['rest_framework.permissions.AllowAny'],
        'password_reset': ['rest_framework.permissions.AllowAny'],
        'password_reset_confirm': ['rest_framework.permissions.AllowAny'],
        'activation': ['core.api.permissions.is_super_user.IsSuperUser'],
        'username_reset': ['core.api.permissions.is_super_user.IsSuperUser'],
        'username_reset_confirm': ['core.api.permissions.is_super_user.IsSuperUser'],
        'set_username': ['core.api.permissions.is_super_user.IsSuperUser'],
        'user_list': ['core.api.permissions.is_super_user.IsSuperUser'],
        'user_delete': ['core.api.permissions.is_super_user.IsSuperUser'],
        'token_create': ['rest_framework.permissions.AllowAny'],
        'token_destroy': ['rest_framework.permissions.IsAuthenticated'],
    },

}