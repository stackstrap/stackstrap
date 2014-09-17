import os
import sh
import shutil
import tempfile

from stackstrap.config import settings
from stackstrap.repository import Repository

from . import StackStrapTestCase


# setup our repo & cache urls & dirs
repo_url = 'https://github.com/stackstrap/stackstrap-test-template.git'
repo_cache_name = ''.join([
    c if c.isalnum() else '-'
    for c in repo_url
])

class RepositoryTestCase(StackStrapTestCase):
    def test_repository_archiving(self):
        """
        Ensure our archive is created properly
        """
        out_dir = tempfile.mkdtemp()
        repo = Repository(repo_url)
        repo.archive('master', out_dir)
        assert os.path.isfile(os.path.join(out_dir, "stackstrap.yml"))
        shutil.rmtree(out_dir)

        out_dir = tempfile.mkdtemp()
        repo = Repository(repo_url)
        repo.archive('missing-meta-for-tests', out_dir)
        assert not os.path.isfile(os.path.join(out_dir, "stackstrap.yml"))
        shutil.rmtree(out_dir)
