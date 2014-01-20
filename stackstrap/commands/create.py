import argparse
import inspect
import os
import re

from stackstrap.commands import Command, CommandError
from stackstrap.project import Project, ProjectException
from stackstrap.template import Template

def name_type(value):
    "This is the argument type that validates project names"

    if not isinstance(value, basestring):
        raise argparse.ArgumentTypeError("You must provide a string value for the project name")

    value = str(value)

    if not re.match(r'[a-z0-9][a-z0-9\-]+', value, re.I):
        raise argparse.ArgumentTypeError(
            "Project names can only contain letters, numbers and dashes."
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
            metavar='TEMPLATE',
            type=str,
            help='The name of the template to use'
        )


    def main(self, args):
        template = Template(args.template)
        if not template.exists:
            raise CommandError("Invalid template: %s" % args.template)

        try:
            project = Project(args.name)
            project.create(template)
        except ProjectException as e:
            raise CommandError(str(e))
