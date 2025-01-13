from .base import *

MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")
INSTALLED_APPS.append("django_browser_reload")
INSTALLED_APPS.append("behave_django")
