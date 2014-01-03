import logging

class Command(object):
    name = 'UNKNOWN'

    def __init__(self):
        self.log = logging.getLogger(self.name)

    def setup_parser(self, parser):
        raise NotImplementedError("The setup_parser method is not implemented in %s" % self.__class__.__name__)

    def main(self, args):
        raise NotImplementedError("The main method is not implemented in %s" % self.__class__.__name__)
