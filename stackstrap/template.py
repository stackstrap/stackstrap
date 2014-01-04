import logging
import os
import sh
import yaml

from stackstrap.config import settings
from stackstrap.repository import Repository

def template_dir(*parts):
    return settings.mkdir('templates', *parts)

def template_path(*parts):
    return settings.path('templates', *parts)

class TemplateException(Exception):
    pass

class TemplateMetaException(TemplateException):
    pass

class TemplateRepoException(TemplateException):
    pass

class Template(object):
    """
    This represents a StackStrap project template
    """
    yaml_attrs = ('name', 'url', 'ref', 'box', 'box_name', 'nopull')

    def __init__(self, name, url, ref, box, box_name=None, nopull=False):
        self.log = logging.getLogger("template")

        self.name = name
        self.url = url
        self.ref = ref
        self.box = box
        if box_name is None:
            self.box_name = os.path.basename(box).strip(".box")
        else:
            self.box_name = box_name
        self.nopull = nopull

        self.template_file = template_path(self.name)
        self.repository = None

        self.validated = False
        self.saved = False

    @classmethod
    def available(cls):
        "Return available templates in our template directory"
        templates = []
        for root, folders, files in os.walk(template_dir()):
            for template in files:
                templates.append(template)

        return templates

    @classmethod
    def load(cls, name):
        "Load an existing template based on its name"
        template_file = template_path(name)
        if os.path.isfile(template_file):
            attrs = yaml.safe_load(open(template_file).read())
            template = cls(**attrs)

            # we mark saved as True since we're loading the template
            template.saved = True
            return template

    @property
    def exists(self):
        "Returns true or false if this template exists in our saved templates"
        return os.path.isfile(self.template_file)

    def validate(self):
        "Setup our repository and ensure the template meta-data is correct"
        self.log.debug("Validating template: %s" % self.name)

        try:
            self.repository = Repository(self.url)
        except sh.ErrorReturnCode as e:
            error_msg = "Failed to setup the repository (%s) for our template (%s): %s" % (
                self.url,
                self.name,
                e
            )
            self.log.error(error_msg)
            raise TemplateRepoException(error_msg)

        # load our yaml from the repository cache
        meta_path = self.repository.cache_path('stackstrap/meta.yml')
        self.log.debug("Loading meta-data from '%s'..." % meta_path)
        try:
            meta_data = open(meta_path).read()
        except OSError as e:
            error_msg = "Failed to read the meta data (%s): %s" % (meta_path, e)
            self.log.error(error_msg)
            raise TemplateMetaException(error_msg)

        self.log.debug("Parsing meta-data...")
        self.log.debug(meta_data)
        try:
            self.meta = yaml.load(meta_data)
        except yaml.error.YAMLError as e:
            error_msg = "Failed to parse the meta-data (%s): %s" % (meta_path, e)
            self.log.error(error_msg)
            raise TemplateMetaException(error_msg)

        self.validated = True
        self.log.debug("Template validated")

    def save(self):
        "Write our YAML file"
        attrs = {}
        for attr in self.yaml_attrs:
            attrs[attr] = getattr(self, attr)

        # call template dir to ensure our template directory exists
        template_dir()

        with open(self.template_file, 'w') as f:
            f.write(yaml.dump(attrs))

        self.saved = True

    def delete(self):
        "Delete our template from the file system"
        os.unlink(self.template_file)

    def archive_to(self, destination, *archive_args):
        "Stub to our repository archive_to method that uses our ref"
        self.repository.archive_to(self.ref, destination, *archive_args)
