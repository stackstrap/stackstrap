import os
import shutil
import tempfile

from stackstrap.cli import StackStrapCLI
from stackstrap.commands import CommandError
from stackstrap.project import Project
from stackstrap.repository import Repository

from . import StackStrapTestCase

repo_url = 'https://github.com/openops/stackstrap-project-template.git'

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
            assert not os.path.isfile(os.path.join(tmp_dir, "test_project_creation", "README.rst"))
            assert not os.path.isfile(os.path.join(tmp_dir, "test_project_creation", "stackstrap.yml"))
        finally:
            os.chdir(orig_dir)
            shutil.rmtree(tmp_dir)

    def test_project_invalid_template(self):
        cli = StackStrapCLI()
        self.assertRaises((CommandError, SystemExit),
                          lambda: cli.main(['create', 'test_project_creation', 'test-template']))
