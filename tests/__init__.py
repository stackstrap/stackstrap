import logging
import os
import shutil
import tempfile
import unittest

from stackstrap.config import settings

class StackStrapTestCase(unittest.TestCase):
    def setUp(self):
        self.log = logging.getLogger("test:%s" % self.__class__.__name__)

        # reconfigure our settings to use a temp directory
        tmp_dir = tempfile.mkdtemp()
        settings.configure(tmp_dir)
        self.log.debug("Configured settings to use: %s" % tmp_dir)

    def tearDown(self):
        # remove the settings directory we setup
        try:
            shutil.rmtree(settings.base_dir)
        except OSError:
            if os.path.isdir(settings.base_dir):
                raise
