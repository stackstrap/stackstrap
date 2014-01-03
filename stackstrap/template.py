import logging
import os
import yaml

TEMPLATE_DIR = os.path.expanduser("~/.stackstrap/templates")
if not os.path.isdir(TEMPLATE_DIR):
    try:
        os.makedirs(TEMPLATE_DIR)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(TEMPLATE_DIR):
            pass
        else:
            raise

class Template(yaml.YAMLObject):
    """
    This represents a StackStrap project template
    """
    template_dir = TEMPLATE_DIR
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!Template'

    def __init__(self, name, url, ref, box, box_name=None, nopull=False):
        self.name = name
        self.url = url
        self.ref = ref
        self.box = box
        if box_name is None:
            self.box_name = os.path.basename(box).strip(".box")
        else:
            self.box_name = box_name
        self.nopull = nopull

        self._template_file = os.path.join(Template.template_dir, self.name)

    @classmethod
    def available(cls):
        "Return available templates in our template directory"
        log = logging.getLogger("templates")
        # TODO: pretty this up
        for root, folders, files in os.walk(Template.template_dir):
            for template in files:
                log.info(template)

    @classmethod
    def load(cls, name):
        "Load an existing template based on its name"
        template_file = os.path.join(Template.template_dir, name)
        if os.path.isfile(template_file):
            return yaml.safe_load(open(template_file).read())

    @property
    def exists(self):
        "Returns true or false if this template exists in our saved templates"
        return os.path.isfile(self._template_file)

    def validate(self):
        pass

    def save(self):
        with open(self._template_file, 'w') as f:
            f.write(yaml.dump(self))
