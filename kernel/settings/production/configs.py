from kernel.settings.config.setup import env

PROTOCOL = env("PROTOCOL")
if PROTOCOL == "https":
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True


CURRENT_SITE = env("CURRENT_SITE")
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = '2525'
EMAIL_USE_TLS = True
Email_USE_SSL = False


MAX_FILE_SIZE = 20

DEFAULT_FROM_EMAIL = 'from@milad.com'

