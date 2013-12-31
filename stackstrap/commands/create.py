import os

from . import Command

from ..repository import Repository

class Create(Command):
    "Creates a new project from a StackStrap template"
    name = 'create'

    def setup_parser(self, parser):
        self.parser = parser

        self.parser.add_argument(
            'name',
            metavar='NAME',
            type=str,
            help='The name of the new project to be created'
        )

        self.parser.add_argument(
            'template',
            metavar='GIT_URL',
            type=str,
            help='The GIT URL of the template to use'
        )

        self.parser.add_argument(
            '--box', '-b',
            metavar='URL',
            type=str,
            help='The url of the Vagrant Box to use, defaults to the official precise32 Box',
            default='http://files.vagrantup.com/precise32.box'
        )
        self.parser.add_argument(
            '--ref', '-r',
            metavar='REF',
            type=str,
            help='The GIT ref of the template to use when creating the project, defaults to master',
            default='master'
        )

    def main(self, args):
        if os.path.exists(args.name):
            self.log.error("The specified name '{name}' already exists".format(
                name=args.name
            ))
            return

        self.log.info("Creating a new project named '{name}' using {template} as the template...".format(
            name=args.name,
            template=args.template
        ))

        self.template_repo = Repository(args.template)
        self.template_repo.archive_to(args.ref, args.name)
