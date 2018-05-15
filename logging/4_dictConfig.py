import logging.config

LOGGING_CONF = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s [%(filename)s:%(lineno)d] %(message)s'
        },
        "onother": {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        "other_cons": {
            "level": "DEBUG",
            'class': 'logging.StreamHandler',
            'formatter': 'onother',
        },
    },
    'loggers': {
        'main': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        "slave": {
            "level": "DEBUG",
            "handlers": ["other_cons"],
        },
    },
}

logging.config.dictConfig(LOGGING_CONF)
