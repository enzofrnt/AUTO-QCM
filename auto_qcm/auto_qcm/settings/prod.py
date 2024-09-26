from .base import *

DEBUG = False

STATIC_ROOT = os.path.join(BASE_DIR.parent, "/app/static")

STATIC_URL = "/static/"

if DEBUG is False:
    MIDDLEWARE.insert(0, "django.middleware.security.SecurityMiddleware")
    MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")

# Configuration de WhiteNoise pour servir les fichiers statiques avec Gunicorn
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost").split(",")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "/app/log/log.txt",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
