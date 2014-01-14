import os

from stackstrap.config import settings
from stackstrap.commands import Command
from stackstrap.template import Template, MASTER_TEMPLATE_URL

class Create(Command):
    "Create a new template"
    name = 'create'

    def setup_parser(self, parser):
        self.parser = parser

        template_url = settings.get('project_template_url',
                                    MASTER_TEMPLATE_URL)

        self.parser.add_argument(
            'path',
            metavar='PATH',
            type=str,
            help='The path to create the new template at'
        )

        self.parser.add_argument(
            '-t', '--template',
            metavar='GIT_URL',
            type=str,
            help='The GIT URL of the template to use. Defaults to %s' % template_url,
            default=template_url
        )

    def main(self, args):
        # this must be imported in here since StackStrapCLI is what initially
        # imports this module
        from stackstrap.cli import StackStrapCLI
        cli = StackStrapCLI()

        template = Template('master-template')
        if not template.exists:
            self.log.info("You are creating a new template for the first time "
                          "we will now setup a template named 'master-template' "
                          "that is used to create new templates.")
            cli.main(['template', 'add', 'master-template', MASTER_TEMPLATE_URL])

        cli.main(['create', args.path, 'master-template'])
