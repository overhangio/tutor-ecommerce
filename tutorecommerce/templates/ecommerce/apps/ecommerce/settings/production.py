from ..production import *

{% include "ecommerce/apps/ecommerce/settings/partials/common.py" %}

MIDDLEWARE = list(MIDDLEWARE)
MIDDLEWARE.insert(0, "whitenoise.middleware.WhiteNoiseMiddleware")

SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = "{% if ACTIVATE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}"

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ ECOMMERCE_OAUTH2_KEY }}"
