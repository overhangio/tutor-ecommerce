from ..devstack import *

{% include "ecommerce/apps/ecommerce/settings/partials/common.py" %}

CORS_ORIGIN_WHITELIST = list(CORS_ORIGIN_WHITELIST)
{% for app_name, app in iter_mfes() %}
{% if app_name == "orders" %}
CORS_ORIGIN_WHITELIST.append("http://{{ MFE_HOST }}:{{ app['port'] }}")
CSRF_TRUSTED_ORIGINS = ["{{ MFE_HOST }}:{{ app['port'] }}"]
{% elif app_name == "payment" %}
CORS_ORIGIN_WHITELIST.append("http://{{ MFE_HOST }}:{{ app['port'] }}")
{% endif %}
{% endfor %}

SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = "http://{{ LMS_HOST }}:8000"

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ ECOMMERCE_OAUTH2_KEY_DEV }}"

{{ patch("ecommerce-settings-development") }}
