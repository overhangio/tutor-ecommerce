import logging.config

from ecommerce_worker.configuration.logger import get_logger_config
from ..base import *

# For the record, we can't import settings from production module because a syslogger is
# configured there.

BROKER_URL = "redis://{% if REDIS_USERNAME and REDIS_PASSWORD %}{{ REDIS_USERNAME }}:{{ REDIS_PASSWORD }}@{% endif %}{{ REDIS_HOST }}:{{ REDIS_PORT }}"

JWT_SECRET_KEY = "{{ JWT_COMMON_SECRET_KEY }}"
JWT_ISSUER = "{{ JWT_COMMON_ISSUER }}"

# Logging: get rid of local handler
logging_config = get_logger_config(
    log_dir="/var/log",
    edx_filename="ecommerce_worker.log",
    dev_env=True,
    debug=False,
    local_loglevel="INFO",
)
logging_config["handlers"].pop("local")
for logger in logging_config["loggers"].values():
    try:
        logger["handlers"].remove("local")
    except ValueError:
        continue
logging.config.dictConfig(logging_config)
