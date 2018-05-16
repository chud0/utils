import logging
import logging.config

DEBUG = True

LOGGING_CONF = {
    "disable_existing_loggers": True,
    "version": 1,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-8s %(asctime)s [%(filename)s:%(lineno)d] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "brief": {
            "format": "%(levelname)-8s %(asctime)s %(name)-16s %(message)s",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "other_cons": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "brief",
        },
    },
    "loggers": {
        "main": {
            "level": "INFO",
            "handlers": ["console"],
        },
        "slave": {
            "level": "DEBUG" if DEBUG else "INFO",
            "handlers": ["other_cons"],
        },
    },
}

logging.config.dictConfig(LOGGING_CONF)

logger = logging.getLogger("main")
logger.info("loggers %s configured", ", ".join(LOGGING_CONF["loggers"]))
