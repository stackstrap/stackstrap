import os
import shutil
import tempfile

from stackstrap.cli import StackStrapCLI
from stackstrap.project import Project
from stackstrap.repository import Repository

from . import StackStrapTestCase

repo_url = 'file://{0}/test_template/'.format(os.path.dirname(__file__))

class ProjectTestCase(StackStrapTestCase):
    def test_project_creation(self):
        orig_dir = os.getcwd()
        tmp_dir = tempfile.mkdtemp()
        os.chdir(tmp_dir)

        cli = StackStrapCLI()
        cli.main(['template', 'add', 'test-template', repo_url])
        cli.main(['create', 'test_project_creation', 'test-template'])

        assert os.path.isfile(os.path.join(tmp_dir, "test_project_creation", "Vagrantfile"))

        assert not os.path.isfile(os.path.join(tmp_dir, "test_project_creation", "README"))
        assert os.path.isfile(os.path.join(tmp_dir, "test_project_creation", "README.transformed"))

        with open(os.path.join(tmp_dir, "test_project_creation", "README.transformed")) as f:
            lines = f.readlines()

        assert lines[0] == "This is a template used to test StackStrap.\n"
        assert lines[1] == "test_project_creation"

        os.chdir(orig_dir)
        shutil.rmtree(tmp_dir)
