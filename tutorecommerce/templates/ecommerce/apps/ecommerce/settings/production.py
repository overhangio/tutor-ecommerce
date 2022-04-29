from ..production import *

{% include "ecommerce/apps/ecommerce/settings/partials/common.py" %}

CORS_ORIGIN_WHITELIST = list(CORS_ORIGIN_WHITELIST) + [
    "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ MFE_HOST }}",
]
CSRF_TRUSTED_ORIGINS = ["{{ MFE_HOST }}"]

SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}"

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ ECOMMERCE_OAUTH2_KEY }}"

{{ patch("ecommerce-settings-production") }}
