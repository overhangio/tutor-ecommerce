from glob import glob
import os

HERE = os.path.abspath(os.path.dirname(__file__))

templates = os.path.join(HERE, "templates")

config = {
    "add": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 20|random_string }}",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
        "API_KEY": "{{ 20|random_string }}",
        "PAYMENT_PROCESSORS": {"cybersource": {}, "paypal": {}},
        "ENABLED_PAYMENT_PROCESSORS": ["cybersource", "paypal"],
        "ENABLED_CLIENT_SIDE_PAYMENT_PROCESSORS": ["cybersource"],
        "EXTRA_PAYMENT_PROCESSOR_CLASSES": [],
    },
    "defaults": {
        "DOCKER_IMAGE": "overhangio/openedx-ecommerce:{{ TUTOR_VERSION }}",
        "WORKER_DOCKER_IMAGE": "overhangio/openedx-ecommerce-worker:{{ TUTOR_VERSION }}",
        "HOST": "ecommerce.{{ LMS_HOST }}",
        "MYSQL_DATABASE": "ecommerce",
        "MYSQL_USERNAME": "ecommerce",
        "MYSQL_USERNAME": "ecommerce",
        "OAUTH2_KEY": "ecommerce",
        "API_TIMEOUT": 5,
        "WORKER_JWT_ISSUER": "ecommerce_worker",
        "EXTRA_PIP_REQUIREMENTS": [],
    },
}

hooks = {
    "build-image": {
        "ecommerce": "{{ ECOMMERCE_DOCKER_IMAGE }}",
        "ecommerce_worker": "{{ ECOMMERCE_WORKER_DOCKER_IMAGE }}",
    },
    "remote-image": {
        "ecommerce": "{{ ECOMMERCE_DOCKER_IMAGE }}",
        "ecommerce_worker": "{{ ECOMMERCE_WORKER_DOCKER_IMAGE }}",
    },
    "init": ["mysql-client", "lms", "ecommerce"],
}


def patches():
    all_patches = {}
    for path in glob(os.path.join(HERE, "patches", "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
