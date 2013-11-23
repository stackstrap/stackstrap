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
        self.assertTrue(os.path.exists(
            "/tmp/stackstrap/private/template_repository_cache/%d/HEAD" % self.template.id
        ))


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

    def assertExists(self, path):
        self.assertTrue(os.path.exists(path))

    def test_add_project(self):
        self.make_project()

        # ensure the keys were generated
        self.assertExists("/tmp/stackstrap/private/keypairs/project-%d.pub" % self.project.id)
        self.assertExists("/tmp/stackstrap/private/keypairs/project-%d.pem" % self.project.id)

        # ensure the keys were installed
        self.assertExists("/tmp/stackstrap/salt/pki/master/minions/project-%d" % self.project.id)

        # ensure it's the right file
        self.assertTrue(filecmp.cmp(
            "/tmp/stackstrap/private/keypairs/project-%d.pub" % self.project.id,
            "/tmp/stackstrap/salt/pki/master/minions/project-%d" % self.project.id
        ))

        # ensure our state & pillar files got installed
        self.assertExists("/tmp/stackstrap/private/project_states/project-%d.sls" % self.project.id)
        self.assertExists("/tmp/stackstrap/private/project_pillars/project-%d.sls" % self.project.id)

    def test_make_zip(self):
        self.make_project()

        c = Client()
        User = get_user_model()
        my_admin = User.objects.create_superuser('root@localhost', 'admin')
        c.login(email='root@localhost', password='admin')
        resp = c.get('/projects/%d/zip' % self.project.id)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'application/x-zip-compressed')

        # ensure it's a valid zip file
        zip_io = StringIO(resp.content)
        z = zipfile.ZipFile(zip_io, "r")

        # valid yaml
        meta = yaml.load(z.read('stackstrap/meta.yml'))

        # ensure the file system transforms happened
        dev = z.read('peanutbutter/peanutbutter/settings/dev.py')

        # and it contains the correct content
        self.assertEqual(str(dev).count("'NAME': 'peanutbutter'"), 1)

        z.close()
