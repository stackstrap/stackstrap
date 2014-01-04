import logging
import os
import shutil
import tempfile
import unittest

from stackstrap.config import settings

base_dir = os.path.dirname(__file__)
test_repos = (
    'test_repo',
    'test_template',
    'test_template_bad',
)

class StackStrapTestCase(unittest.TestCase):
    def setUp(self):
        self.log = logging.getLogger("test:%s" % self.__class__.__name__)

        # reconfigure our settings to use a temp directory
        tmp_dir = tempfile.mkdtemp()
        settings.configure(tmp_dir)
        self.log.debug("Configured settings to use: %s" % tmp_dir)

        self.git_fixup('_git', '.git')

    def tearDown(self):
        # restore the .git dirs back to _git
        self.git_fixup('.git', '_git')

        # remove the settings directory we setup
        try:
            shutil.rmtree(settings.base_dir)
        except OSError:
            if os.path.isdir(settings.base_dir):
                raise

    def git_fixup(self, orig, dest):
        # Since we can't distribute a git respository in a git repository we use a
        # hack and keep the .git dir as _git. This renames them back to .git
        for repo in test_repos:
            orig_path = os.path.join(base_dir, repo, orig)
            dest_path = os.path.join(base_dir, repo, dest)
            self.log.debug("Renaming %s -> %s" % (orig_path, dest_path))
            try:
                shutil.move(orig_path, dest_path)
            except IOError:
                if not os.path.isdir(dest_path):
                    raise
