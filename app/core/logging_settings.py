from app.core.settings import settings

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
            "level": "DEBUG" if settings.debug_mode else "INFO",
            "formatter": "detailed",
            "filename": settings.log_file_path,
            "maxBytes": settings.log_file_max_size,
            "backupCount": settings.log_file_backup_count,
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
