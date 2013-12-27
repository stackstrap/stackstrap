from garment import *
from garment.vagrant import vagrant

import fabric.api as fab

@fab.task
def django_admin(command):
    vagrant.sudo('/bin/sh -c ". /home/stackstrap/virtualenv/bin/activate; PYTHONPATH=/home/stackstrap/current/application/stackstrap DJANGO_SETTINGS_MODULE=stackstrap.settings.dev django-admin.py %s"' % command, user='stackstrap')

@fab.task
def runserver():
    django_admin("runserver 0:6000")
