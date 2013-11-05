from .base import *

try:
    import yaml

    with open('/etc/salt/minion.d/stackstrap.conf', 'r') as f:
        grains = yaml.load(f.read())
    config = grains.get('stackstrap', {})
except:
    config = {}

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    config.get('allowed_hosts', config.get('hostname', 'stackstrap-master.local'))
    ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stackstrap',
        'USER': 'stackstrap',
    }
}

MEDIA_ROOT = '/home/stackstrap/domains/stackstrap-master/media'
MEDIA_URL = '/media/'

STATIC_ROOT = '/home/stackstrap/domains/stackstrap-master/static'
STATIC_URL = '/static/'
