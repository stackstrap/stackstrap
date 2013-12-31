import errno
import inspect
import logging
import os
import sh
import tempfile

def mkdir_p(path):
    try:
        os.makedirs(path, 0755)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

class Repository(object):
    "Represents a GIT Repository and allows for easy operations"

    _git = None

    @property
    def git(self):
        if not self._git:
            self._git = sh.git.bake(_cwd=self.path, _env={
                'GIT_SSH': self.loose_ssh
            })
        return self._git

    def __init__(self, url):
        self.url = url
        self.log = logging.getLogger("repository")

        self.repo_cache = os.path.expanduser('~/.stackstrap/repository_cache/')
        self.path = os.path.join(
            self.repo_cache,
            "".join([
                c if c.isalnum() else '-'
                for c in url
            ])
        )

        self.loose_ssh = os.path.join(
            os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),
            "loose_ssh.sh"
        )

        if os.path.exists(self.path):
            self.log.debug("Repository already exists in our cache, pulling from origin...")
            self.git('pull', 'origin')
            self.git('submodule', 'update')
        else:
            self.log.debug("Creating a new copy of the repository in our cache, cloning...")
            mkdir_p(self.path)
            self.git('clone', '--recurse-submodules', url, '.')

    def archive_to(self, git_ref, destination, *archive_args):
        self.log.debug("Archiving '{ref}' to {destination}".format(
            ref=git_ref,
            destination=destination
        ))

        try:
            mkdir_p(destination)

            (fd, tar_file) = tempfile.mkstemp()
            self.git.archive("remotes/origin/%s" % git_ref, *archive_args, _out=tar_file)
            sh.tar("xf", tar_file, _cwd=destination)
        finally:
            if tar_file:
                os.remove(tar_file)
