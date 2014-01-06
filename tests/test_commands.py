from stackstrap.cli import StackStrapCLI
from stackstrap.commands import CommandLoader, Command

from . import StackStrapTestCase

class CLITestCase(StackStrapTestCase):
    def test_cli_success(self):
        cli = StackStrapCLI()
        cli.main(['template', 'list'])

    def test_cli_failure(self):
        cli = StackStrapCLI()

        # use assertRaises as a context manager so we get the exit code
        # see: http://stackoverflow.com/a/15672165
        with self.assertRaises(SystemExit) as cm:
            cli.main(['template', 'remove', 'doesntexist'])
        self.assertEqual(cm.exception.code, 1)


class CommandLoaderTestCase(StackStrapTestCase):
    def test_missing_subparsers(self):
        class MissingSubparsers(CommandLoader):
            pass

        loader = MissingSubparsers()
        self.assertRaises(NotImplementedError, loader.load_commands)


class CommandTestCase(StackStrapTestCase):
    def test_command_implementation(self):
        class BadCommand(Command):
            pass

        command = BadCommand()
        self.assertRaises(NotImplementedError, lambda: command.setup_parser(None))
        self.assertRaises(NotImplementedError, lambda: command.main(None))

