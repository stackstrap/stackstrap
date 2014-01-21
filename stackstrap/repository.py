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

    def archive(self, ref, destination, *archive_args):
        """
        Archive the specified GIT ref to the specified destination

        Any extra args are passed to the sh command directly so you can
        add extra flags for `git archive` should you desire.
        """
        tmp_dir = tempfile.mkdtemp()
        tar_file = None

        try:
            # create our git interface via the sh module
            # see:
            # github.com/freesurface/stackstrap/blob/master/scripts/loose_ssh.sh
            git = sh.git.bake(_cwd=tmp_dir, _env={
                'GIT_SSH': "loose_ssh.sh"
            })

            self.log.debug("Cloning %s to %s" % (self.url, tmp_dir))
            git('clone', '--recursive', self.url, tmp_dir)

            self.log.debug("Archiving '{ref}' to {destination}".format(
                ref=ref,
                destination=destination
            ))

            settings.mkdir_p(destination)

            (fd, tar_file) = tempfile.mkstemp()
            git.archive('origin/%s' % ref, *archive_args, _out=tar_file)
            sh.tar("xpf", tar_file, _cwd=destination)
        finally:
            if tar_file:
                os.remove(tar_file)

            if os.path.isdir(tmp_dir):
                shutil.rmtree(tmp_dir)
