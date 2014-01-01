import argparse
import logging

from stackstrap.commands.create import Create

from stackstrap import __version__

class StackStrapCLI(object):
    """
    The main CLI interface for StackStrap
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Making development with Vagrant + Salt more awesome'
        )

        self.subparsers = self.parser.add_subparsers(
            title='commands',
            description='',
            help='',
            dest='command'
        )

        self.parser.add_argument(
            '-V', '--version',
            action='version',
            version=__version__
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
        parser = self.subparsers.add_parser(
            command.name,
            help=command.__doc__
        )
        command.setup_parser(parser)

        self.commands[command.name] = command

    def main(self):
        args = self.parser.parse_args()

        log_level = logging.INFO
        log_format = '%(message)s'
        if args.quiet:
            log_level = logging.WARN
        elif args.debug:
            log_level = logging.DEBUG
            log_format = '[%(asctime)s] %(name)s - %(levelname)s: %(message)s'

        logging.basicConfig(level=log_level, format=log_format)
        self.log = logging.getLogger("main")

        self.log.debug("StackStrap starting up")
        self.log.debug("Command: %s" % args.command)

        self.commands[args.command].main(args)
