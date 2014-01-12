import logging

from stackstrap.commands import Command, CommandLoader

from stackstrap.commands.template.add import Add
from stackstrap.commands.template.create import Create
from stackstrap.commands.template.list import List
from stackstrap.commands.template.remove import Remove

class Template(Command, CommandLoader):
    "Manages templates"
    name = 'template'
    commands_to_load = (Add, Create, List, Remove) 

    def setup_parser(self, parser):
        self.parser = parser

        self.subparsers = self.parser.add_subparsers(
            title='actions',
            description='',
            help='',
            dest='action'
        )

        self.load_commands()

    def main(self, args):
        "Delegate to our commands"
        self.commands[args.action].main(args)
