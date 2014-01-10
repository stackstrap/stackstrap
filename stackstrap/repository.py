import logging
import os
import sh
import shutil
import tempfile

from stackstrap.config import settings

REPOSITORY_CACHE = 'repository_cache'


class Repository(object):
    "Represents a GIT Repository and allows for easy operations"

    def __init__(self, url):
        self.log = logging.getLogger("repository")
        self.url = url

    def archive_to(self, git_ref, destination, *archive_args):
        """
        Archive the specified GIT ref to the specified destination

        Any extra args are passed to the sh command directly so you can
        add extra flags for `git archive` should you desire.
        """
        tmp_dir = tempfile.mkdtemp()

        # create our git interface via the sh module
        # the loose_ssh.sh script is a simple wrapper that sets:
        #     StrictHostKeyChecking=no
        #
        # see:
        # github.com/openops/stackstrap/blob/master/scripts/loose_ssh.sh
        self.git = sh.git.bake(_cwd=tmp_dir, _env={
            'GIT_SSH': "loose_ssh.sh"
        })

        self.log.debug("Creating a new copy of the repository in our \
                        cache (%s)..." % self.path)
        self.git('clone', '--recursive', self.url, tmp_dir)

        self.log.debug("Archiving '{ref}' to {destination}".format(
            ref=git_ref,
            destination=destination
        ))

        tar_file = None
        settings.mkdir_p(destination)

        try:
            (fd, tar_file) = tempfile.mkstemp()
            self.git.archive(git_ref,
                             *archive_args, _out=tar_file)
            sh.tar("xf", tar_file, _cwd=destination)
        finally:
            if tar_file:
                os.remove(tar_file)
            shutil.rmtree(tmp_dir)

    def cache_path(self, *parts):
        return os.path.join(self.path, *parts)
