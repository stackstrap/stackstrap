import os
import shutil

base_dir = os.path.dirname(__file__)
test_repos = (
    'test_repo',
    'test_template'
)

def setup_repositories():
    """
    Since we can't distribute a git respository in a git repository we use a
    hack and keep the .git dir as _git. This renames them back to .git
    """
    for repo in test_repos:
        shutil.move(os.path.join(base_dir, repo, '_git'),
                    os.path.join(base_dir, repo, '.git'))

def restore_repositories():
    for repo in test_repos:
        shutil.move(os.path.join(base_dir, repo, '.git'),
                    os.path.join(base_dir, repo, '_git'))
