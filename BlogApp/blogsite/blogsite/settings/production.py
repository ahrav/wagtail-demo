from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': '/cloudsql/speedy-realm-252106:us-central1:wagtail-demo-db',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'randopass'
    }
}

SECRET_KEY = 'supersecret'

ALLOWED_HOSTS = ['speedy-realm-252106.appspot.com']

try:
    from .local import *
except ImportError:
    pass
