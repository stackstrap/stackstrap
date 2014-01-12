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
        self.parser.add_argument(
            '-f', '--force',
            dest='force',
            action='store_true',
            help='Do not prompt when over-writing an existing template',
            default=False
        )

    def main(self, args):
        template = Template(args.name)

        if template.exists:
            if args.force:
                self.log.info("Template '%s' already exists. Force has been specified, overwriting it.")
            else:
                response = raw_input("The template '%s' already exists. Overwrite it? [y/n]:" % args.name)
                if response not in ('y', 'Y', 'yes', 'YES', 'Yes'):
                    return

        template.create(args.url, args.ref)

        self.log.info("Created new template: %s" % args.name)
