import os
import sh
import shutil
import tempfile

from stackstrap.config import settings
from stackstrap.repository import Repository

from . import StackStrapTestCase


# setup our repo & cache urls & dirs
repo_url = 'file://{0}/test_repo/'.format(os.path.dirname(__file__))
repo_cache_name = ''.join([
    c if c.isalnum() else '-'
    for c in repo_url
])

class RepositoryTestCase(StackStrapTestCase):
    def test_repository_creation(self):
        """
        Ensure our repository creation works as expected
        """
        repo_cache_dir = settings.path('repository_cache', repo_cache_name)
        self.assertFalse(os.path.isdir(repo_cache_dir))

        repo = Repository(repo_url)

        self.assertTrue(os.path.isdir(repo_cache_dir))
        self.assertTrue(os.path.isfile(os.path.join(repo_cache_dir, "README")))

        shutil.rmtree(repo_cache_dir)


    def test_repository_archiving(self):
        """
        Ensure our archive is created properly
        """
        out_dir = tempfile.mkdtemp()
        repo = Repository(repo_url)
        repo.archive_to('master', out_dir)
        assert os.path.isfile(os.path.join(out_dir, "README"))
        assert not os.path.isfile(os.path.join(out_dir, "OTHER"))
        shutil.rmtree(out_dir)

        out_dir = tempfile.mkdtemp()
        repo = Repository(repo_url)
        repo.archive_to('other', out_dir)
        assert os.path.isfile(os.path.join(out_dir, "README"))
        assert os.path.isfile(os.path.join(out_dir, "OTHER"))
        shutil.rmtree(out_dir)
