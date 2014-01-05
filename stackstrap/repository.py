import errno
import logging
import os
import sh
import tempfile

from stackstrap.config import settings

REPOSITORY_CACHE = 'repository_cache'

class Repository(object):
    "Represents a GIT Repository and allows for easy operations"

    def __init__(self, url, nopull=False):
        self.log = logging.getLogger("repository")
        self.url = url

        self.cache_id = "".join([
            c if c.isalnum() else '-'
            for c in url
        ])

        # ensure the top level cache dir exists and construct our path
        settings.mkdir(REPOSITORY_CACHE)
        self.path = settings.path(REPOSITORY_CACHE, self.cache_id)

        # create our git interface via the sh module
        # the loose_ssh.sh script is a simple wrapper that sets:
        #     StrictHostKeyChecking=no
        #
        # see: https://github.com/fatbox/stackstrap/blob/master/scripts/loose_ssh.sh
        self.git = sh.git.bake(_cwd=self.path, _env={
            'GIT_SSH': "loose_ssh.sh"
        })

        # if our path exists then the repository already exists, do a pull
        # otherwise clone it into the directory
        if os.path.exists(self.path):
            if nopull:
                self.log.debug("Skipping pull")
            else:
                self.log.debug("Repository already exists in our cache (%s), pulling from origin..." % self.path)
                self.git('pull', 'origin')
                self.git('submodule', 'update')
        else:
            self.log.debug("Creating a new copy of the repository in our cache (%s)..." % self.path)
            settings.mkdir_p(self.path)
            self.git('clone', '--recurse-submodules', url, '.')

    def archive_to(self, git_ref, destination, *archive_args):
        """
        Archive the specified GIT ref to the specified destination

        Any extra args are passed to the sh command directly so you can
        add extra flags for `git archive` should you desire.
        """
        self.log.debug("Archiving '{ref}' to {destination}".format(
            ref=git_ref,
            destination=destination
        ))

        tar_file = None
        settings.mkdir_p(destination)

        try:
            (fd, tar_file) = tempfile.mkstemp()
            self.git.archive("remotes/origin/%s" % git_ref, *archive_args, _out=tar_file)
            sh.tar("xf", tar_file, _cwd=destination)
        finally:
            if tar_file:
                os.remove(tar_file)

    def cache_path(self, *parts):
        return os.path.join(self.path, *parts)
