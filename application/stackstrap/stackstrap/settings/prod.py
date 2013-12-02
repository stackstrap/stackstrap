from .base import *

try:
    import yaml

    with open('/etc/salt/minion.d/stackstrap.conf', 'r') as f:
        yaml_data = yaml.load(f.read())
    config = yaml_data.get('grains', {}).get('stackstrap', {})
except:
    config = {}

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    config.get('allowed_hosts', config.get('http_server_name', 'stackstrap-master'))
    ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stackstrap',
        'USER': 'stackstrap',
    }
}

PRIVATE_ROOT = '/home/stackstrap/private'

MEDIA_ROOT = '/home/stackstrap/media'
MEDIA_URL = '/media/'

STATIC_ROOT = '/home/stackstrap/static'
STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'default': {
            'level': 'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': "/home/stackstrap/logs/application.log",
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}
