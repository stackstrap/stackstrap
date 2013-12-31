import os
import yaml

from . import Command
from ..repository import Repository
from ..template import Template

class Create(Command):
    "Creates a new project from a StackStrap template"
    name = 'create'

    def setup_parser(self, parser):
        self.parser = parser

        self.parser.add_argument(
            'name',
            metavar='NAME',
            type=str,
            help='The name of the new project to be created'
        )

        self.parser.add_argument(
            'template',
            metavar='GIT_URL',
            type=str,
            help='The GIT URL of the template to use'
        )

        self.parser.add_argument(
            '-b', '--box',
            dest='box',
            metavar='URL',
            type=str,
            help='The url of the Vagrant Box to use, defaults to the official precise32 Box',
            default='http://files.vagrantup.com/precise32.box'
        )
        self.parser.add_argument(
            '-r', '--ref',
            dest='ref',
            metavar='REF',
            type=str,
            help='The GIT ref of the template to use when creating the project, defaults to master',
            default='master'
        )

    def main(self, args):
        if os.path.exists(args.name):
            self.log.error("The specified name '{name}' already exists".format(
                name=args.name
            ))
            return

        self.log.info("Creating a new project named '{name}' using {template} as the template...".format(
            name=args.name,
            template=args.template
        ))

        # access the repository and archive it to our destination project name
        template_repo = Repository(args.template)
        template_repo.archive_to(args.ref, args.name)

        # for backwards compatibility we provide a mock project object
        class Project(object):
            short_name = args.name

        # build our global context
        template_context = {
            'name': args.name,
            'box_url': args.box,
            'box_name': os.path.basename(args.box).strip(".box"),

            # see above
            'project': Project()
        }

        # create our template interface
        template = Template(
            globals=template_context,
            file_loader_paths=[os.path.abspath(args.name)]
        )

        def mkdir(*parts):
            return os.mkdir(os.path.join(args.name, *parts), 0755)

        def path(*parts):
            return os.path.join(args.name, *parts)

        def render(dest, source):
            with open(dest, 'w') as f:
                f.write(template.render(source))

        def render_in_place(source):
            data = open(source).read()
            with open(source, 'w') as f:
                f.write(template.render_string(data))

        mkdir('salt')
        mkdir('salt', 'root')

        render(path('Vagrantfile'), 'Vagrantfile')
        render(path('salt', 'minion'), 'salt.minion')

        # read the meta-data
        # it must be processed as a template, then loaded as YAML
        metadata = yaml.load(template.render('stackstrap/meta.yml'))

        # iterate the files to parse with Django templates
        file_template_paths = metadata.get("file_templates", [])
        file_template_paths.append("stackstrap/meta.yml")
        for p in file_template_paths:
            render_in_place(path(p))

        # iterate the paths to update with custom names
        path_templates = metadata.get("path_templates", [])
        for path_template in path_templates:
            for orig_path in path_template:
                os.rename(path(orig_path),
                          path(path_template[orig_path]))

        self.log.info("Done!\nYou can now 'vagrant up' your development environment from the {name} folder".format(
            name=args.name
        ))
