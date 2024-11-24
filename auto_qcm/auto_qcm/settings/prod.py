from .base import *

DEBUG = False

STATIC_ROOT = os.path.join(BASE_DIR.parent, "/app/static")

STATIC_URL = "/static/"

if DEBUG is False:
    mddlwr_security_index = MIDDLEWARE.index(
        "django.middleware.security.SecurityMiddleware"
    )
    MIDDLEWARE.insert(
        mddlwr_security_index + 1, "whitenoise.middleware.WhiteNoiseMiddleware"
    )

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost").split(",")
if ALLOWED_HOSTS == [""]:
    ALLOWED_HOSTS = ["localhost"]

CSRF_TRUSTED_ORIGINS = os.environ.get(
    "DJANGO_CSRF_TRUSTED_ORIGINS", "http://localhost"
).split(",")
if CSRF_TRUSTED_ORIGINS == [""]:
    CSRF_TRUSTED_ORIGINS = ["http://localhost"]

INSTALLED_APPS.append("django_minify_html")

MIDDLEWARE += (
    "django.middleware.gzip.GZipMiddleware",
    "django_minify_html.middleware.MinifyHtmlMiddleware",
)

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
