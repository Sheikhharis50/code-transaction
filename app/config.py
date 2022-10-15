"""
Logging configurations
"""

LOGGING = {
    "version": 1,
    "formatters": {
        "std_out": {
            "format": (
                "[%(asctime)s][%(levelname)s]"
                "[%(module)s][%(funcName)s]"
                "[%(thread)d, %(threadName)s]: %(message)s"
            ),
            "datefmt": "%d-%m-%Y %I:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "formatter": "std_out",
            "class": "logging.StreamHandler",
            "level": "INFO",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
