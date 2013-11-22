try:
  from cStringIO import StringIO
except:
  from StringIO import StringIO

import filecmp
import os
import shutil
import yaml
import zipfile

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from .models import Project, Template, Box

class ProjectTestCase(TestCase):
    def setUp(self):
        self.box = Box.objects.create(
            name='precise32',
            url='http://files.vagrantup.com/precise32.box'
        )

        # create the template
        self.template = Template.objects.create(
            name='Django',
            git_url='https://github.com/fatbox/stackstrap-django.git'
        )

        # ensure the local repository cache got checked out
        self.assertTrue(os.path.exists("/tmp/stackstrap/private/template_repository_cache/1/HEAD"))

    def tearDown(self):
        shutil.rmtree("/tmp/stackstrap/private/template_repository_cache/1", ignore_errors=True)


class ProjectTests(ProjectTestCase):
    def make_project(self):
        # create the project
        self.project = Project.objects.create(
            name='Django Test',
            short_name='peanutbutter',
            description='Just a test project',
            box=self.box,
            template=self.template
        )

    def test_add_project(self):
        self.make_project()

        # ensure the keys were generated
        self.assertTrue(os.path.exists("/tmp/stackstrap/private/keypairs/project-1.pub"))
        self.assertTrue(os.path.exists("/tmp/stackstrap/private/keypairs/project-1.pem"))

        # ensure the keys were installed
        self.assertTrue(os.path.exists("/tmp/stackstrap/salt/pki/master/minions/project-1"))

        # ensure it's the right file
        self.assertTrue(filecmp.cmp(
            "/tmp/stackstrap/private/keypairs/project-1.pub",
            "/tmp/stackstrap/salt/pki/master/minions/project-1"
        ))

        # ensure our state & pillar files got installed
        self.assertTrue(os.path.exists("/tmp/stackstrap/private/project_states/project-1.sls"))
        self.assertTrue(os.path.exists("/tmp/stackstrap/private/project_pillars/project-1.sls"))

    def test_make_zip(self):
        self.make_project()

        c = Client()
        User = get_user_model()
        my_admin = User.objects.create_superuser('root@localhost', 'admin')
        c.login(email='root@localhost', password='admin')
        resp = c.get('/projects/1/zip')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'application/x-zip-compressed')

        # ensure it's a valid zip file
        zip_io = StringIO(resp.content)
        with zipfile.ZipFile(zip_io, "r") as z:
            # valid yaml
            meta = yaml.load(z.read('stackstrap/meta.yml'))

            # ensure the file system transforms happened
            dev = z.read('peanutbutter/peanutbutter/settings/dev.py')

            # and it contains the correct content
            self.assertEqual(str(dev).count("'NAME': 'peanutbutter'"), 1)
