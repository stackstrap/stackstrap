import random
import string

from jinja2 import Template, Environment, \
                   ChoiceLoader, FileSystemLoader

def random_secret(length=96):
    "Generates a long, random string to be used as secret keys in applications"
    pool = string.ascii_letters + string.digits
    return "".join([
        random.choice(pool)
        for x in xrange(length)
        ])

class JinjaInterface(object):
    """
    An interface to render files & strings using Jinja2
    """
    def __init__(self, file_loader_paths=[], globals={}):
        loaders = [
            FileSystemLoader(path)
            for path in file_loader_paths
        ]

        self.env = Environment(
            loader=ChoiceLoader(loaders),
            extensions=('jinja2.ext.do', 'jinja2.ext.loopcontrols')
        )

        # add our global functions
        globals['random_secret'] = random_secret

        self.env.globals = globals

    def render_file(self, name, context={}):
        template = self.env.get_template(name)
        return template.render(**context)

    def render_string(self, string, context={}):
        template = self.env.from_string(string)
        return template.render(**context)
