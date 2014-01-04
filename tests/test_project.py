import os
import shutil
import tempfile

from stackstrap.project import Project
from stackstrap.repository import Repository

from . import StackStrapTestCase
from .test_template import make_template

class ProjectTestCase(StackStrapTestCase):
    def test_project_creation(self):
        orig_dir = os.getcwd()
        tmp_dir = tempfile.mkdtemp()
        os.chdir(tmp_dir)

        template = make_template()
        project = Project("test_project_creation", template)
        project.create()

        assert os.path.isfile(os.path.join(tmp_dir, "test_project_creation", "Vagrantfile"))

        assert not os.path.isfile(os.path.join(tmp_dir, "test_project_creation", "README"))
        assert os.path.isfile(os.path.join(tmp_dir, "test_project_creation", "README.transformed"))

        with open(os.path.join(tmp_dir, "test_project_creation", "README.transformed")) as f:
            lines = f.readlines()

        assert lines[0] == "This is a template used to test StackStrap.\n"
        assert lines[1] == "test_project_creation"

        os.chdir(orig_dir)
        shutil.rmtree(tmp_dir)
