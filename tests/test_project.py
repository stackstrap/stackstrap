import argparse
import os
import shutil
import tempfile

from stackstrap.cli import StackStrapCLI
from stackstrap.commands import CommandError
from stackstrap.commands.create import name_type
from stackstrap.project import Project
from stackstrap.repository import Repository

from . import StackStrapTestCase

repo_url = 'https://github.com/stackstrap/stackstrap-test-template.git'

class ProjectTestCase(StackStrapTestCase):
    def test_project_creation(self):
        orig_dir = os.getcwd()
        tmp_dir = tempfile.mkdtemp()
        try:
            os.chdir(tmp_dir)

            self.log.debug("Test project creation dir: %s" % tmp_dir)

            cli = StackStrapCLI()
            cli.main(['template', 'add', 'test-template', repo_url])
            cli.main(['create', 'test_project_creation', 'test-template'])

            assert os.path.isfile(os.path.join(tmp_dir, "test_project_creation", "Vagrantfile"))
            assert os.path.isfile(os.path.join(tmp_dir, "test_project_creation", "README"))
            assert not os.path.isfile(os.path.join(tmp_dir, "test_project_creation", "README.md"))
        finally:
            os.chdir(orig_dir)
            shutil.rmtree(tmp_dir)

    def test_project_duplicate_creation(self):
        orig_dir = os.getcwd()
        tmp_dir = tempfile.mkdtemp()
        try:
            os.chdir(tmp_dir)

            cli = StackStrapCLI()
            cli.main(['template', 'add', 'test-template', repo_url])
            cli.main(['create', 'test_project_creation', 'test-template'])
            try:
                cli.main(['create', 'test_project_creation', 'test-template'])
                raise Exception("This shouldn't be reached")
            except SystemExit as e:
                self.assertEqual(e.code, 1)
        finally:
            os.chdir(orig_dir)
            shutil.rmtree(tmp_dir)

    def test_project_invalid_name(self):
        self.assertRaises(argparse.ArgumentTypeError, lambda: name_type(1))
        self.assertRaises(argparse.ArgumentTypeError, lambda: name_type('!@#$%^'))

    def test_project_invalid_template(self):
        cli = StackStrapCLI()
        self.assertRaises((CommandError, SystemExit),
                          lambda: cli.main(['create', 'test_project_creation', 'test-template']))
