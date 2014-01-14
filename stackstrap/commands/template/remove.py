from stackstrap.commands import Command, CommandError
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
        template = Template(args.name)
        if not template.exists:
            raise CommandError("Invalid template name: %s" % args.name)

        self.log.info("Removing template '%s'" % template.name)
        template.delete()
