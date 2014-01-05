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
            '-P', '--nopull',
            dest='nopull',
            action='store_true',
            help='Skip pulling from origin prior to creation',
            default=False
        )
        self.parser.add_argument(
            '-b', '--box',
            dest='box',
            metavar='URL',
            type=str,
            help='The url of the Vagrant Box to use, defaults to the official precise32 Box',
            default='http://files.vagrantup.com/precise32.box'
        )
        self.parser.add_argument(
            '-B', '--box-name',
            dest='box_name',
            metavar='NAME',
            type=str,
            help='The name of the box, defaults to being automatically derived from the URL',
            default=None
        )
        self.parser.add_argument(
            '-f', '--force',
            dest='force',
            action='store_true',
            help='Do not prompt when over-writing an existing template',
            default=False
        )

    def main(self, args):
        template = Template(
            args.name,
            args.url,
            args.ref,
            args.box,
            box_name=args.box_name,
            nopull=args.nopull
        )

        if template.exists and not args.force:
            response = raw_input("The template '%s' already exists. Overwrite it? [y/n]:" % args.name)
            if response not in ('y', 'Y', 'yes', 'YES', 'Yes'):
                return

        template.validate()
        template.save()

        self.log.info("Created new template: %s" % args.name)
