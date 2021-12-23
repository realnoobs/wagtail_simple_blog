import os
import django_heroku
import dj_database_url
from .base import *  # NOQA

DEBUG = False

MIDDLEWARE += ["whitenoise.middleware.WhiteNoiseMiddleware"]  # NOQA
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
DEFAULT_FILE_STORAGE = "storages.backends.dropbox.DropBoxStorage"
DROPBOX_OAUTH2_TOKEN = os.environ.get("DROPBOX_OAUTH2_TOKEN")
DROPBOX_ROOT_PATH = os.environ.get("DROPBOX_ROOT_PATH", '/')
DROPBOX_TIMEOUT = os.environ.get("DROPBOX_TIMEOUT", 100)
DROPBOX_WRITE_MODE = os.environ.get("DROPBOX_WRITE_MODE", "add")

DATABASES["default"] = dj_database_url.config(conn_max_age=600)  # NOQA
SECRET_KEY = os.environ.setdefault(
    "SECRET_KEY", "django-insecure-$^@)vl_4p-+de31n)gn6)80vgfgmy)s+cqh$nzx=^dv$h(kw&p8"
)

# try:
#     from .local import *  # NOQA
# except ImportError:
#     pass

django_heroku.settings(locals())
