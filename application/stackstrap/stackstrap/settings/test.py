from .base import *

import errno
import shutil
import os

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def rm_fr(path):
    try:
        shutil.rmtree(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.ENOENT:
            pass
        else:
            raise

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_stackstrap',
        'USER': 'postgres'
    }
}

SALT_PKI_ROOT = '/tmp/stackstrap/salt/pki'

PRIVATE_ROOT = '/tmp/stackstrap/private'

MEDIA_ROOT = '/tmp/stackstrap/media'
MEDIA_URL = '/media/'

STATIC_ROOT = '/tmp/stackstrap/static'
STATIC_URL = '/static/'

for dirname in (SALT_PKI_ROOT, PRIVATE_ROOT, MEDIA_ROOT, STATIC_ROOT,
                os.path.join(SALT_PKI_ROOT, "master", "minions"),
                os.path.join(PRIVATE_ROOT, "project_pillars"),
                os.path.join(PRIVATE_ROOT, "project_states")):
    rm_fr(dirname)
    mkdir_p(dirname)
