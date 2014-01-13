import logging

class CommandError(Exception):
    pass

class CommandLoader(object):
    """
    CommandLoader is a mixin that loads a tuple of Commands and creates them
    each as a subparser, calling their setup_parser method
    """
    commands_to_load = tuple()
    subparsers = None

    def load_commands(self):
        "Iterates and instantiates all of the commands marked to load"
        if self.subparsers is None:
            raise NotImplementedError("The class %s needs to have a 'subparsers' attribute prior to calling load_commands" %
                                      self.__class__.__name__)

        self.commands = {}
        for cls in self.commands_to_load:
            command = cls()
            parser = self.subparsers.add_parser(
                command.name,
                help=command.__doc__
            )
            command.setup_parser(parser)

            self.commands[command.name] = command


class Command(object):
    """
    Classes being loaded through the CommandLoader should include this mixin.
    It provides the basic skeleton that each command should have and sets up
    a logger object for the command
    """
    name = 'UNKNOWN'

    def __init__(self):
        self.log = logging.getLogger(self.name)

    def setup_parser(self, parser):
        raise NotImplementedError("The setup_parser method is not implemented in %s" % self.__class__.__name__)

    def main(self, args):
        raise NotImplementedError("The main method is not implemented in %s" % self.__class__.__name__)
