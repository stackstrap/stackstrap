from .base import *

# In dev mode we use eth1 as the master interface since Vagrant configures a
# private network on eth0 and puts our bridge on eth1
MASTER_INTERFACE = 'eth1'

DEBUG = True
TEMPLATE_DEBUG = True

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
