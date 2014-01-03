import argparse
import inspect
import os
import re

from stackstrap.commands import Command
from stackstrap.repository import Repository
from stackstrap.project import Project

def name_type(value):
    "This is the argument type that validates project names"

    if not isinstance(value, basestring):
        raise argparse.ArgumentTypeError("You must provide a string value for the project name")

    value = str(value)

    if not re.match(r'[a-z0-9][a-z0-9\-]+', value, re.I):
        raise argparse.ArgumentTypeError(
            "Project names can only contain letters, numbers and dashes."
            "This is a restriction imposed because the project name is used as"
            "the hostname for Vagrant"
        )

    return value

class Create(Command):
    "Creates a new project from a StackStrap template"
    name = 'create'

    def setup_parser(self, parser):
        self.parser = parser

        self.parser.add_argument(
            'name',
            metavar='NAME',
            type=name_type,
            help='The name of the new project to be created'
        )

        self.parser.add_argument(
            'template',
            metavar='GIT_URL',
            type=str,
            help='The GIT URL of the template to use'
        )


    def main(self, args):
        template_repo = Repository(args.template, nopull=args.nopull)
        project = Project(args.name, template_repo)
        project.create(args.ref, args.box, box_name=args.box_name)
