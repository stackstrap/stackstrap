import inspect
import logging
import os
import sh
import shutil
import tempfile
import yaml

from stackstrap.config import settings
from stackstrap.repository import Repository

MASTER_TEMPLATE_URL = 'https://github.com/freesurface/stackstrap-master-template.git'

def template_dir(*parts):
    return settings.mkdir('templates', *parts)


def template_path(*parts):
    return settings.path('templates', *parts)


class TemplateException(Exception):
    pass

class TemplateExists(TemplateException):
    pass

class TemplateMetaException(TemplateException):
    pass

class TemplateRepoException(TemplateException):
    pass


class Template(object):
    """
    This represents a StackStrap project template
    """
    @classmethod
    def available(cls):
        "Return available templates in our template directory"
        return [
            item
            for item in os.listdir(template_dir())
        ]

    def __init__(self, name):
        self.log = logging.getLogger("template")

        self.name = name
        self.path = template_path(self.name)

        self.validated = False

    @property
    def exists(self):
        "Returns true or false if this template exists in our saved templates"
        return os.path.exists(template_path(self.name))

    def setup(self, url, ref):
        "Archives our repository to our path and validates the template"
        if self.exists:
            raise TemplateExists("A template named '%s' already exists" % self.name)

        tmp_dir = tempfile.mkdtemp()

        try:
            repo = Repository(url)
            repo.archive(ref, tmp_dir)

            self.validate(tmp_dir)

            shutil.move(tmp_dir, self.path)
        except sh.ErrorReturnCode as e:
            error_msg = "Failed to setup the repository (%s) \
                         for our template (%s): %s" % (
                        url,
                        self.name,
                        e
                    )
            self.log.error(error_msg)
            raise TemplateRepoException(error_msg)
        finally:
            if os.path.isdir(tmp_dir):
                shutil.rmtree(tmp_dir)

    def validate(self, path=None):
        "Setup our repository and ensure the template meta-data is correct"
        if path is None:
            path = self.path

        self.log.debug("Validating template: %s (%s)" % (self.name, path))

        def _path(*parts):
            return os.path.join(path, *parts)

        # load our yaml from the repository cache
        meta_path = _path('stackstrap.yml')
        self.log.debug("Loading meta-data from '%s'..." % meta_path)
        try:
            meta_data = open(meta_path).read()
        except (OSError, IOError) as e:
            error_msg = "Failed to read the meta data (%s): \
                         %s" % (meta_path, e)
            self.log.error(error_msg)
            raise TemplateMetaException(error_msg)

        self.log.debug("Parsing meta-data...")
        try:
            self.meta = yaml.load(meta_data)
        except yaml.error.YAMLError as e:
            error_msg = "Failed to parse the meta-data (%s): \
                         %s" % (meta_path, e)
            self.log.error(error_msg)
            raise TemplateMetaException(error_msg)

        required_attrs = (
            'template_name',
            'template_description'
        )

        for attr in required_attrs:
            if attr not in self.meta:
                error_msg = "Missing template meta data: %s" % attr
                self.log.error(error_msg)
                raise TemplateMetaException(error_msg)

            self.log.debug(" - %s: %s" % (attr, self.meta[attr]))

        self.validated = True
        self.log.debug("Template validated")

    def delete(self):
        "Delete our template from the file system"
        if self.exists:
            shutil.rmtree(self.path)

    def copy_to(self, destination):
        "Copy our template to a new path"
        if self.exists:
            shutil.copytree(self.path, destination)
