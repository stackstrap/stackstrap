import os
import shutil
import tempfile

from nose import with_setup

from stackstrap.project import Project
from stackstrap.repository import Repository

from . import setup_repositories, restore_repositories

# setup our repo & cache urls & dirs
repo_url = 'file://{0}/test_template/'.format(os.path.dirname(__file__))

@with_setup(setup_repositories, restore_repositories)
def test_project_creation():
    orig_dir = os.getcwd()
    tmp_dir = tempfile.mkdtemp()
    os.chdir(tmp_dir)

    repository = Repository(repo_url)
    project = Project("test_project_creation", repository)
    project.create("master", "http://files.vagrantup.com/precise32.box")

    assert not os.path.isfile(os.path.join(tmp_dir, "test_project_creation", "README"))
    assert os.path.isfile(os.path.join(tmp_dir, "test_project_creation", "README.transformed"))

    with open(os.path.join(tmp_dir, "test_project_creation", "README.transformed")) as f:
        lines = f.readlines()

    assert lines[0] == "This is a template used to test StackStrap.\n"
    assert lines[1] == "test_project_creation"

    os.chdir(orig_dir)
    shutil.rmtree(tmp_dir)
