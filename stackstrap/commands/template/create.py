import os

from stackstrap.commands import Command
from stackstrap.template import Template

class Create(Command):
    "Create a new template"
    name = 'create'

    def setup_parser(self, parser):
        self.parser = parser

        self.parser.add_argument(
            'path',
            metavar='PATH',
            type=str,
            help='The path to create the new template at'
        )

        self.parser.add_argument(
            '-n', '--name',
            metavar='NAME',
            type=str,
            help='The name of the template, defaults to the path basename'
        )

    def main(self, args):
        Template.create(args.path, args.name)
