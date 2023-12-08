from __future__ import annotations

import os
import typing as t
from glob import glob

import pkg_resources
from tutor import hooks as tutor_hooks
from tutor.__about__ import __version_suffix__
from tutormfe.hooks import MFE_APPS, MFE_ATTRS_TYPE

from .__about__ import __version__

# Handle version suffix in nightly mode, just like tutor core
if __version_suffix__:
    __version__ += "-" + __version_suffix__

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
        "WORKER_JWT_ISSUER": "ecommerce-worker",  # TODO do we need to keep this?
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
}


@MFE_APPS.add()  # type: ignore
def _add_ecommerce_mfe_apps(
    apps: dict[str, MFE_ATTRS_TYPE]
) -> dict[str, MFE_ATTRS_TYPE]:
    apps.update(
        {
            "orders": {
                "repository": "https://github.com/edx/frontend-app-ecommerce",
                "port": 7296,
            },
            "payment": {
                "repository": "https://github.com/edx/frontend-app-payment",
                "port": 1998,
            },
        }
    )
    return apps


# Initialization hooks
for service in ("mysql", "lms", "ecommerce"):
    with open(
        os.path.join(
            pkg_resources.resource_filename("tutorecommerce", "templates"),
            "ecommerce",
            "tasks",
            service,
            "init",
        ),
        encoding="utf-8",
    ) as task_file:
        tutor_hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, task_file.read()))

# Image management
tutor_hooks.Filters.IMAGES_BUILD.add_items(
    [
        (
            "ecommerce",
            ("plugins", "ecommerce", "build", "ecommerce"),
            "{{ ECOMMERCE_DOCKER_IMAGE }}",
            (),
        ),
        (
            "ecommerce-worker",
            ("plugins", "ecommerce", "build", "ecommerce-worker"),
            "{{ ECOMMERCE_WORKER_DOCKER_IMAGE }}",
            (),
        ),
    ]
)
tutor_hooks.Filters.IMAGES_PULL.add_items(
    [
        (
            "ecommerce",
            "{{ ECOMMERCE_DOCKER_IMAGE }}",
        ),
        (
            "ecommerce-worker",
            "{{ ECOMMERCE_WORKER_DOCKER_IMAGE }}",
        ),
    ]
)
tutor_hooks.Filters.IMAGES_PUSH.add_items(
    [
        (
            "ecommerce",
            "{{ ECOMMERCE_DOCKER_IMAGE }}",
        ),
        (
            "ecommerce-worker",
            "{{ ECOMMERCE_WORKER_DOCKER_IMAGE }}",
        ),
    ]
)
for mfe in ["orders", "payment"]:
    name = f"{mfe}-dev"
    tag = "{{ DOCKER_REGISTRY }}overhangio/openedx-" + mfe + "-dev:{{ MFE_VERSION }}"
    tutor_hooks.Filters.IMAGES_BUILD.add_item(
        (
            name,
            ("plugins", "mfe", "build", "mfe"),
            tag,
            (f"--target={mfe}-dev",),
        )
    )
    tutor_hooks.Filters.IMAGES_PULL.add_item((name, tag))
    tutor_hooks.Filters.IMAGES_PUSH.add_item((name, tag))

####### Boilerplate code
# Add the "templates" folder as a template root
tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutorecommerce", "templates")
)
# Render the "build" and "apps" folders
tutor_hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("ecommerce/build", "plugins"),
        ("ecommerce/apps", "plugins"),
    ],
)
# Load patches from files
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorecommerce", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        tutor_hooks.Filters.ENV_PATCHES.add_item(
            (os.path.basename(path), patch_file.read())
        )
# Add configuration entries
tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"ECOMMERCE_{key}", value) for key, value in config.get("defaults", {}).items()]
)
tutor_hooks.Filters.CONFIG_UNIQUE.add_items(
    [(f"ECOMMERCE_{key}", value) for key, value in config.get("unique", {}).items()]
)
tutor_hooks.Filters.CONFIG_OVERRIDES.add_items(
    list(config.get("overrides", {}).items())
)


@tutor_hooks.Filters.APP_PUBLIC_HOSTS.add()
def _print_ecommerce_public_hosts(
    hosts: list[str], context_name: t.Literal["local", "dev"]
) -> list[str]:
    if context_name == "dev":
        hosts += ["{{ ECOMMERCE_HOST }}:8130"]
    else:
        hosts += ["{{ ECOMMERCE_HOST }}"]
    return hosts


# Automount /openedx/ecommerce folder from the container
@tutor_hooks.Filters.COMPOSE_MOUNTS.add()
def _mount_ecommerce_apps(
    mounts: list[tuple[str, str]], path_basename: str
) -> list[tuple[str, str]]:
    if path_basename == "ecommerce":
        mounts += [("ecommerce", "/openedx/ecommerce")]
    elif path_basename == "frontend-app-ecommerce":
        # payment MFE will be handled by the tutor-mfe plugin, but we need to fix the
        # auto-mount for the ecommerce/order MFE
        mounts.remove(("ecommerce", "/openedx/app"))
        mounts.append(("orders", "/openedx/app"))
    return mounts


# Bind-mount repo at build-time, both for prod and dev images
@tutor_hooks.Filters.IMAGES_BUILD_MOUNTS.add()
def _mount_ecommerce_on_build(
    mounts: list[tuple[str, str]], host_path: str
) -> list[tuple[str, str]]:
    path_basename = os.path.basename(host_path)
    if path_basename == "ecommerce":
        mounts.append(("ecommerce", "ecommerce-src"))
    elif path_basename == "frontend-app-ecommerce":
        # payment MFE will be handled by the tutor-mfe plugin, but we need to fix the
        # auto-mount for the ecommerce/order MFE
        mounts.remove(("mfe", "ecommerce-src"))
        mounts.remove(("ecommerce-dev", "ecommerce-src"))
        mounts.append(("mfe", "orders-src"))
        mounts.append(("orders-dev", "orders-src"))
    return mounts
