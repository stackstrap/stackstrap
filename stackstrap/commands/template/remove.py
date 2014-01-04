from stackstrap.commands import Command
from stackstrap.template import Template

class Remove(Command):
    "Remove a template"
    name = 'remove'

    def setup_parser(self, parser):
        self.parser = parser
        self.parser.add_argument(
            'name',
            metavar='NAME',
            help='The name of the template to remove'
        )

    def main(self, args):
        template = Template.load(args.name)
        if not template:
            self.log.error("Invalid template name: %s" % args.name)
            return

        self.log.info("Removing template '%s'" % template.name)
        template.delete()
