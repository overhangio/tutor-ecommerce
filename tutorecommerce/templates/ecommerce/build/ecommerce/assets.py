from .base import *

# Get rid of local logger
LOGGING["handlers"].pop("local")
for logger in LOGGING["loggers"].values():
    logger["handlers"].remove("local")

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
