import logging
import logging.config
import queue
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

log_que = queue.Queue(-1)

LOGGING_CONF = {
    "disable_existing_loggers": True,
    "version": 1,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-8s %(asctime)s [%(filename)s:%(lineno)d] %(message)s",
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
        "smtp_mail": {
            "level": "INFO",
            "class": "logging.handlers.SMTPHandler",
            "formatter": "brief",
            "mailhost": mailhost,
            "fromaddr": fromaddr,
            "toaddrs": toaddr,
            "subject": subject,
            "credentials": credentials,
            "secure": (),
        },
        "queue_handler": {
            "level": "INFO",
            "class": "logging.handlers.QueueHandler",
            "formatter": "brief",
            "queue": log_que,
        },
    },
    "loggers": {
        "main": {
            "level": "DEBUG",
            "handlers": ["console", "queue_handler"],
        },
        "sendmail": {
            "level": "DEBUG",
            "handlers": ["smtp_mail"],
        }
    },
}

logging.config.dictConfig(LOGGING_CONF)
listener = logging.handlers.QueueListener(log_que, *logging.getLogger("sendmail").handlers)
listener.start()

logger = logging.getLogger("main")
logger.info("loggers %s configured", ", ".join(LOGGING_CONF["loggers"]))

logger.error("ura)))")
logger.warning("test")

import time
time.sleep(15)
# listener.stop()
