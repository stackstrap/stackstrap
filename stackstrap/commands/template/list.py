from stackstrap.commands import Command
from stackstrap.template import Template

class List(Command):
    "List all templates"
    name = 'list'

    def setup_parser(self, parser):
        pass

    def main(self, args):
        # TODO: pretty this output up
        for template in Template.available():
            self.log.info(template)
