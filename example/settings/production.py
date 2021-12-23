import os
import django_heroku
import dj_database_url
from .base import *  # NOQA

DEBUG = False

MIDDLEWARE += ["whitenoise.middleware.WhiteNoiseMiddleware"]  # NOQA
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
DEFAULT_FILE_STORAGE = "storages.backends.dropbox.DropBoxStorage"
DROPBOX_OAUTH2_TOKEN = os.getenv("DROPBOX_OAUTH2_TOKEN")
DROPBOX_ROOT_PATH = os.getenv("DROPBOX_ROOT_PATH", "/")
DROPBOX_TIMEOUT = os.getenv("DROPBOX_TIMEOUT", 100)
DROPBOX_WRITE_MODE = os.getenv("DROPBOX_WRITE_MODE", "add")

DATABASES["default"] = dj_database_url.config(conn_max_age=600)  # NOQA
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure")

# try:
#     from .local import *  # NOQA
# except ImportError:
#     pass

django_heroku.settings(locals())
