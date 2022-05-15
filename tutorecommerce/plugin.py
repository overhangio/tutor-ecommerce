from glob import glob
import os
import pkg_resources

from tutor import hooks as tutor_hooks

from .__about__ import __version__

config = {
    "defaults": {
        "VERSION": __version__,
        "API_TIMEOUT": 5,
        "CURRENCY": "USD",
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-ecommerce:{{ ECOMMERCE_VERSION }}",
        "WORKER_DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-ecommerce-worker:{{ ECOMMERCE_VERSION }}",
        "EXTRA_PIP_REQUIREMENTS": [],
        "HOST": "ecommerce.{{ LMS_HOST }}",
        "MYSQL_DATABASE": "ecommerce",
        "MYSQL_USERNAME": "ecommerce",
        "OAUTH2_KEY": "ecommerce",
        "OAUTH2_KEY_DEV": "ecommerce-dev",
        "OAUTH2_KEY_SSO": "ecommerce-sso",
        "OAUTH2_KEY_SSO_DEV": "ecommerce-sso-dev",
        "CUSTOM_THEME_REPOSITORY_URL": "",
        "CUSTOM_THEME_NAME": "edx-theme",
        "WORKER_JWT_ISSUER": "ecommerce-worker",  # TODO do we need to keep this?
        # Micro frontend applications
        "MFE_APP": {
            "name": "orders",
            "repository": "https://github.com/edx/frontend-app-ecommerce",
            "port": 1996,
        },
        "PAYMENT_MFE_APP": {
            "name": "payment",
            "repository": "https://github.com/edx/frontend-app-payment",
            "port": 1998,
            "env": {
                "production": {
                    # Hardcoded in edx-platform
                    "CURRENCY_COOKIE_NAME": "edx-price-l10n",
                    # TODO set customizable value
                    "CYBERSOURCE_URL": "https://testsecureacceptance.cybersource.com/silent/pay",
                    "SUPPORT_URL": "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}/support",
                },
                "development": {
                    "SUPPORT_URL": "http://{{ LMS_HOST }}:8000/support",
                },
            },
        },
    },
    "unique": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 20|random_string }}",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
        "OAUTH2_SECRET_SSO": "{{ 8|random_string }}",
        "API_KEY": "{{ 20|random_string }}",
        "PAYMENT_PROCESSORS": {
            "cybersource": {
                "flex_shared_secret_key_id": "SET-ME-PLEASE",
                "flex_shared_secret_key": "SET-ME-PLEASE",
                "merchant_id": "SET-ME-PLEASE",
                "soap_api_url": "https://ics2wstest.ic3.com/commerce/1.x/transactionProcessor/CyberSourceTransaction_1.140.wsdl",
                "transaction_key": "SET-ME-PLEASE",
            },
            "paypal": {
                "mode": "sandbox",
                "client_id": "SET-ME-PLEASE",
                "client_secret": "SET-ME-PLEASE",
                "cancel_checkout_path": "/checkout/cancel-checkout/",
                "error_url": "/checkout/error/",
                "receipt_url": "/checkout/receipt/",
            },
        },
        "ENABLE_IDENTITY_VERIFICATION": True,
        "ENABLED_PAYMENT_PROCESSORS": ["cybersource", "paypal"],
        "ENABLED_CLIENT_SIDE_PAYMENT_PROCESSORS": ["cybersource"],
        "EXTRA_PAYMENT_PROCESSOR_CLASSES": [],
        "EXTRA_PAYMENT_PROCESSOR_URLS": {},
    },
    "overrides": {
    },
}

################# Initialization tasks
tutor_hooks.Filters.COMMANDS_INIT.add_item(
    (
        "lms",
        ("ecommerce", "hooks", "lms", "init"),
    )
)
tutor_hooks.Filters.COMMANDS_INIT.add_item(
    (
        "ecommerce",
        ("ecommerce", "hooks", "ecommerce", "init"),
    )
)
tutor_hooks.Filters.COMMANDS_INIT.add_item(
    (
        "mysql",
        ("ecommerce", "hooks", "mysql", "init"),
    )
)
tutor_hooks.Filters.IMAGES_BUILD.add_item(
    (
        "ecommerce",
        #("ecommerce", "hooks", "ecommerce", "build"),
        ("plugins", "ecommerce", "build", "ecommerce"),
        "{{ ECOMMERCE_DOCKER_IMAGE }}",
        (),
    )
)
#tutor_hooks.Filters.IMAGES_BUILD.add_item(
#    (
#        "ecommerce-worker",
#        ("plugins", "ecommerce", "build", "ecommerce-worker"),
#        "{{ ECOMMERCE_WORKER_DOCKER_IMAGE }}",
#        (),
#    )
#)

@tutor_hooks.Filters.IMAGES_PULL.add()
@tutor_hooks.Filters.IMAGES_PUSH.add()
def _add_remote_ecommerce_image_iff_customized(images, user_config):
    """
    Register ECOMMERCE image for pushing & pulling if and only if it has
    been set to something other than the default.

    This is work-around to an upstream issue with ECOMMERCE config. Briefly:
    User config is baked into ECOMMERCE builds, so Tutor cannot host a generic
    pre-built ECOMMERCE image. Howevever, individual Tutor users may want/need to
    build and host their own ECOMMERCE image. So, as a compromise, we tell Tutor
    to push/pull the ECOMMERCE image if the user has customized it to anything
    other than the default image URL.
    """
    image_tag = user_config["ECOMMERCE_DOCKER_IMAGE"]
    if not image_tag.startswith("docker.io/overhangio/openedx-ecommerce:"):
        # Image has been customized. Add to list for pulling/pushing.
        images.append(("ecommerce", image_tag))

    #image_tag = user_config["ECOMMERCE_WORKER_DOCKER_IMAGE"]
    #if not image_tag.startswith("docker.io/overhangio/openedx-ecommerce-worker:"):
    #    images.append(("ecommerce-worker", image_tag))

    return images


################# You don't really have to bother about what's below this line,
################# except maybe for educational purposes :)

# Plugin templates
tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutorecommerce", "templates")
)
tutor_hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("ecommerce/build", "plugins"),
        ("ecommerce/apps", "plugins"),
    ],
)
# Load all patches from the "patches" folder
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorecommerce", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        tutor_hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))

# Load all configuration entries
tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        (f"ECOMMERCE_{key}", value)
        for key, value in config["defaults"].items()
    ]
)
tutor_hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        (f"ECOMMERCE_{key}", value)
        for key, value in config["unique"].items()
    ]
)
tutor_hooks.Filters.CONFIG_OVERRIDES.add_items(list(config["overrides"].items()))
