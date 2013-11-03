from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stackstrap',
        'USER': 'stackstrap',
    }
}

MEDIA_ROOT = '/home/stackstrap/media'
MEDIA_URL = '/media/'

STATIC_ROOT = '/home/stackstrap/static'
STATIC_URL = '/static/'
