from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'oi5&2ybbtbgii$kfgp6i@&f2r!^4p&l!&gcd(-n$87rot2tb=z'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = INSTALLED_APPS + [
    # 'debug_toolbar',
    'django_extensions',
    'wagtail.contrib.styleguide',
]

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': 'randopass'
#     }
# }

MIDDLEWARE = MIDDLEWARE + [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ('127.0.0.1', '172.17.01')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/Users/ahrav/Wagtail/BlogApp/blogsite/blogsite/cache',
    }
}

try:
    from .local import *
except ImportError:
    pass
