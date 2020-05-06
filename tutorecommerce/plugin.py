from glob import glob
import os

from .__about__ import __version__

HERE = os.path.abspath(os.path.dirname(__file__))

templates = os.path.join(HERE, "templates")

config = {
    "add": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 20|random_string }}",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
        "API_KEY": "{{ 20|random_string }}",
        "PAYMENT_PROCESSORS": {
            "cybersource": {
                "merchant_id": "SET-ME-PLEASE",
                "profile_id": "SET-ME-PLEASE",
                "access_key": "SET-ME-PLEASE",
                "secret_key": "SET-ME-PLEASE",
                "transaction_key": "SET-ME-PLEASE",
                "payment_page_url": "https://testsecureacceptance.cybersource.com/pay",
                "receipt_page_url": "/checkout/receipt/",
                "cancel_checkout_path": "/checkout/cancel-checkout/",
                "soap_api_url": "https://ics2wstest.ic3.com/commerce/1.x/transactionProcessor/CyberSourceTransaction_1.140.wsdl",
                "send_level_2_3_details": True,
                "sop_profile_id": "SET-ME-PLEASE",
                "sop_access_key": "SET-ME-PLEASE",
                "sop_secret_key": "SET-ME-PLEASE",
                "sop_payment_page_url": "https://testsecureacceptance.cybersource.com/silent/pay",
            },
            "paypal": {
                "mode": "sandbox",
                "client_id": "SET-ME-PLEASE",
                "client_secret": "SET-ME-PLEASE",
                "receipt_url": "/checkout/receipt/",
                "cancel_checkout_path": "/checkout/cancel-checkout/",
                "error_url": "/checkout/error/",
            },
        },
        "ENABLED_PAYMENT_PROCESSORS": ["cybersource", "paypal"],
        "ENABLED_CLIENT_SIDE_PAYMENT_PROCESSORS": ["cybersource"],
        "EXTRA_PAYMENT_PROCESSOR_CLASSES": [],
    },
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "overhangio/openedx-ecommerce:{{ ECOMMERCE_VERSION }}",
        "WORKER_DOCKER_IMAGE": "overhangio/openedx-ecommerce-worker:{{ ECOMMERCE_VERSION }}",
        "HOST": "ecommerce.{{ LMS_HOST }}",
        "MYSQL_DATABASE": "ecommerce",
        "MYSQL_USERNAME": "ecommerce",
        "OAUTH2_KEY": "ecommerce",
        "API_TIMEOUT": 5,
        "WORKER_JWT_ISSUER": "ecommerce-worker",
        "EXTRA_PIP_REQUIREMENTS": [],
    },
}

hooks = {
    "build-image": {
        "ecommerce": "{{ DOCKER_REGISTRY }}{{ ECOMMERCE_DOCKER_IMAGE }}",
        "ecommerce-worker": "{{ DOCKER_REGISTRY }}{{ ECOMMERCE_WORKER_DOCKER_IMAGE }}",
    },
    "remote-image": {
        "ecommerce": "{{ DOCKER_REGISTRY }}{{ ECOMMERCE_DOCKER_IMAGE }}",
        "ecommerce-worker": "{{ DOCKER_REGISTRY }}{{ ECOMMERCE_WORKER_DOCKER_IMAGE }}",
    },
    "init": ["mysql", "lms", "ecommerce"],
}


def patches():
    all_patches = {}
    for path in glob(os.path.join(HERE, "patches", "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
