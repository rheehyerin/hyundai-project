import os
from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, "..", "staticfiles")


DATABASES = { 'default': {
'ENGINE': 'django.db.backends.postgresql', 'hyundai_project': 'ubuntu',
'USER': 'ubuntu',
'PASSWORD': 'withaskdjango!',
'HOST': '127.0.0.1', },
}
