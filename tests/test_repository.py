import os
import shutil
import tempfile

from stackstrap.repository import Repository

# setup our repo & cache urls & dirs
repo_url = 'file://{0}/test_repo/'.format(os.path.dirname(__file__))
repo_cache_name = ''.join([
    c if c.isalnum() else '-'
    for c in repo_url
])
cache_dir = os.path.expanduser('~/.stackstrap/repository_cache')
repo_cache_dir = os.path.join(cache_dir, repo_cache_name)

def test_repository_creation():
    """
    Ensure our repository creation sets up the cache dir correctly and that
    the cloning process works as expected
    """
    if os.path.isdir(repo_cache_dir):
        shutil.rmtree(repo_cache_dir)
    assert not os.path.isdir(repo_cache_dir)

    repo = Repository(repo_url)
    assert os.path.isdir(repo_cache_dir)
    assert os.path.isfile(os.path.join(repo_cache_dir, "README"))

def test_repository_cache_dir():
    """
    Ensure creation works when we specify a different cache_dir
    """
    cache_dir = tempfile.mkdtemp()
    repo_cache_dir = os.path.join(cache_dir, repo_cache_name)
    assert not os.path.isdir(repo_cache_dir)

    repo = Repository(repo_url, cache_dir=cache_dir)
    assert os.path.isdir(repo_cache_dir)

    shutil.rmtree(cache_dir)

def test_repository_archiving():
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
