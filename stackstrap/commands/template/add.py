from stackstrap.commands import Command
from stackstrap.template import Template

class Add(Command):
    "Add a new template"
    name = 'add'

    def setup_parser(self, parser):
        self.parser = parser

        self.parser.add_argument(
            'name',
            metavar='NAME',
            type=str,
            help='The name of the new template'
        )
        self.parser.add_argument(
            'url',
            metavar='GIT_URL',
            type=str,
            help='The GIT URL of the template'
        )
        self.parser.add_argument(
            '-r', '--ref',
            dest='ref',
            metavar='REF',
            type=str,
            help='The GIT ref of the template to use when creating projects, defaults to master',
            default='master'
        )

    def main(self, args):
        template = Template(args.name)

        if template.exists:
            self.log.error("The template '%s' already exists")
            return

        template.setup(args.url, args.ref)

        self.log.info("Created new template: %s" % args.name)
