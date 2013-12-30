from . import Command

class Create(Command):
    name = 'create'

    def setup_parser(self):
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
            help='The url of the Vagrant Box to use, defaults to the official precise32 Box'
        )
