class Command(object):
    name = 'UNKNOWN'

    def register_parsers(self, subparsers):
        self.parser = subparsers.add_parser(self.name)
        self.setup_parser()

    def setup_parser(self):
        raise NotImplemented("The setup_parser method is not implemented in %s" % self.__class__.__name__)
