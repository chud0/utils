import logging.config
from os import getenv

MAIL_HOST = getenv('MAIL_HOST')
MAIL_PORT = getenv('MAIL_PORT')
MAIL_LOGIN = getenv('MAIL_LOGIN')
MAIL_PASSWORD = getenv('MAIL_PASSWORD')

MAIL_FROM = getenv('MAIL_FROM')
MAIL_TO = getenv('MAIL_TO')

mailhost = (MAIL_HOST, MAIL_PORT)
fromaddr = MAIL_FROM
toaddr = MAIL_TO
subject = "TEST"
credentials = (MAIL_LOGIN, MAIL_PASSWORD)

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
        "mail": {
            "level": "INFO",
            "class": "logging.handlers.SMTPHandler",
            "formatter": "brief",
            "mailhost": mailhost,
            "fromaddr": fromaddr,
            "toaddrs": toaddr,
            "subject": subject,
            "credentials": credentials,
            "secure": (),
        }
    },
    "loggers": {
        "main": {
            "level": "DEBUG",
            "handlers": ["console", "mail"],
        },
    },
}

logging.config.dictConfig(LOGGING_CONF)

logger = logging.getLogger("main")
logger.info("loggers %s configured", ", ".join(LOGGING_CONF["loggers"]))
