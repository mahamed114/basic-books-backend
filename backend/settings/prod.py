from decouple import config
import django_on_heroku

from .base import *

SECRET_KEY = config("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = [
    "basicbooks.herokuapp.com",
    "books.basicbooks.com",
    "basicbooks.com",
]


CORS_ALLOWED_ORIGINS = [
    "https://basicbooks.com",
    "https://books.basicbooks.com",
]


# Staticfiles
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

# Heroku Logging
DEBUG_PROPAGATE_EXCEPTIONS = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "MYAPP": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}


# Heroku Settings
django_on_heroku.settings(locals())
del DATABASES["default"]["OPTIONS"]["sslmode"]
