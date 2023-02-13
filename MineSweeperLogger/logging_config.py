from MineSwLogger import DEBUG
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
        },
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
            # "level": "DEBUG",
            "handlers": ["other_cons"],
        },
    },
}