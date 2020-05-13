# -*- coding: utf-8 -*-

import json
from .production import *

LOGGING["handlers"]["console"]["level"] = "DEBUG"  # TODO remove me
LOGGING["handlers"]["local"]["level"] = "DEBUG"  # TODO remove me

SECRET_KEY = "{{ ECOMMERCE_SECRET_KEY }}"
ALLOWED_HOSTS = [
    "{{ ECOMMERCE_HOST }}",
    "localhost",
    "ecommerce",
    "ecommerce.localhost",
]
PLATFORM_NAME = "{{ PLATFORM_NAME }}"
PROTOCOL = "{% if ACTIVATE_HTTPS %}https{% else %}http{% endif %}"

EDX_API_KEY = "{{ ECOMMERCE_API_KEY }}"
JWT_AUTH = {
    "JWT_SECRET_KEY": "{{ OPENEDX_SECRET_KEY }}",
    "JWT_ISSUERS": [
        {
            "ISSUER": "{{ JWT_COMMON_ISSUER }}",
            "AUDIENCE": "{{ JWT_COMMON_AUDIENCE }}",
            "SECRET_KEY": "{{ JWT_COMMON_SECRET_KEY }}",
        },
        {
            "ISSUER": "{{ ECOMMERCE_WORKER_JWT_ISSUER }}",
            "AUDIENCE": "{{ JWT_COMMON_AUDIENCE }}",
            "SECRET_KEY": "{{ JWT_COMMON_SECRET_KEY }}",
        },
    ],
    "JWT_VERIFY_AUDIENCE": False,
    "JWT_DECODE_HANDLER": "ecommerce.extensions.api.handlers.jwt_decode_handler",
}

SOCIAL_AUTH_EDX_OIDC_SECRET = "{{ ECOMMERCE_OAUTH2_SECRET }}"
SOCIAL_AUTH_EDX_OIDC_ID_TOKEN_DECRYPTION_KEY = SOCIAL_AUTH_EDX_OIDC_SECRET
SOCIAL_AUTH_EDX_OIDC_ISSUER = "{{ JWT_COMMON_ISSUER }}"
SOCIAL_AUTH_REDIRECT_IS_HTTPS = {% if ACTIVATE_HTTPS %}True{% else %}False{% endif %}
SOCIAL_AUTH_EDX_OIDC_KEY = "{{ ECOMMERCE_OAUTH2_KEY }}"
SOCIAL_AUTH_EDX_OIDC_URL_ROOT = "{% if ACTIVATE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}/oauth2"
SOCIAL_AUTH_EDX_OIDC_PUBLIC_URL_ROOT = SOCIAL_AUTH_EDX_OIDC_URL_ROOT
SOCIAL_AUTH_EDX_OIDC_LOGOUT_URL = "{% if ACTIVATE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}/logout"
SOCIAL_AUTH_EDX_OAUTH2_ISSUER = SOCIAL_AUTH_EDX_OIDC_URL_ROOT
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = SOCIAL_AUTH_EDX_OIDC_URL_ROOT

EDX_DRF_EXTENSIONS = {
    'OAUTH2_USER_INFO_URL': '{% if ACTIVATE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}/oauth2/user_info',
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "{{ ECOMMERCE_MYSQL_DATABASE }}",
        "USER": "{{ ECOMMERCE_MYSQL_USERNAME }}",
        "PASSWORD": "{{ ECOMMERCE_MYSQL_PASSWORD }}",
        "HOST": "{{ MYSQL_HOST }}",
        "PORT": "{{ MYSQL_PORT }}",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "{{ SMTP_HOST }}"
EMAIL_PORT = "{{ SMTP_PORT }}"
EMAIL_HOST_USER = "{{ SMTP_USERNAME }}"
EMAIL_HOST_PASSWORD = "{{ SMTP_PASSWORD }}"
EMAIL_USE_TLS = {{SMTP_USE_TLS}}

ENTERPRISE_SERVICE_URL = '{% if ACTIVATE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}/enterprise/'
ENTERPRISE_API_URL = urljoin(ENTERPRISE_SERVICE_URL, 'api/v1/')

LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": "/var/log/ecommerce.log",
    "formatter": "standard",
}

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

PAYMENT_PROCESSOR_CONFIG = {
    "openedx": json.loads("""{{ ECOMMERCE_PAYMENT_PROCESSORS|tojson(indent=4) }}""")
}
PAYMENT_PROCESSORS = list(PAYMENT_PROCESSORS) + {{ ECOMMERCE_EXTRA_PAYMENT_PROCESSOR_CLASSES }}
