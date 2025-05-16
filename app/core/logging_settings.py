from app.core.config import (
    DEBUG_MODE,
    LOG_FILE_BACKUP_COUNT,
    LOG_FILE_MAX_SIZE,
    LOG_FILE_PATH,
)

LOGGING_SETTINGS = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "detailed": {
            "format": "%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
        },
        "rotating_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG" if DEBUG_MODE else "INFO",
            "formatter": "detailed",
            "filename": LOG_FILE_PATH,
            "maxBytes": LOG_FILE_MAX_SIZE,
            "backupCount": LOG_FILE_BACKUP_COUNT,
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "RagNotesAI": {
            "level": "DEBUG",
            "handlers": ["console", "rotating_file"],
            "propagate": False,
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "rotating_file"]
    }
}
