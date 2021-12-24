from .base import *  # NOQA

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
INTERNAL_IPS = [
    "127.0.0.1",
]
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%*rvl_4p-+de31n)gn6)80vgfgmy)s+cqh$nzx=^dv$h(kw&p8"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]
MIDDLEWARE += [  # NOQA
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
INSTALLED_APPS += [  # NOQA
    "debug_toolbar",
]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
