import argparse
import logging

from .commands.create import Create

from . import __version__

class StackStrapCLI(object):
    """
    The main CLI interface for StackStrap
    """

    def __init__(self):
        self.log = logging.getLogger(__name__)

        self.parser = argparse.ArgumentParser(
            description='Making development with Vagrant + Salt suck less'
        )

        self.subparsers = self.parser.add_subparsers(
            title='commands',
            description='available commands',
            help=''
        )

        self.parser.add_argument(
            '-V', '--version',
            action='version',
            version=__version__
        )

        self.parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            dest='verbose',
            help='more verbose output'
        )

        self.parser.add_argument(
            '-d', '--debug',
            action='store_true',
            dest='debug',
            help='copious amounts of output'
        )

        self.parser.add_argument(
            '-q', '--quiet',
            action='store_true',
            dest='quiet',
            help='show only warnings and errors'
        )

        self.commands = {}
        self.add_command(Create())

    def add_command(self, command):
        command.register_parsers(self.subparsers)

        self.commands[command.name] = command

    def main(self):
        args = self.parser.parse_args()
