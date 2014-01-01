import inspect
import os
import shutil
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
            '-B', '--box-name',
            dest='box_name',
            metavar='NAME',
            type=str,
            help='The name of the box, defaults to being automatically derived from the URL'
        )
        self.parser.add_argument(
            '-r', '--ref',
            dest='ref',
            metavar='REF',
            type=str,
            help='The GIT ref of the template to use when creating the project, defaults to master',
            default='master'
        )
        self.parser.add_argument(
            '-P', '--nopull',
            dest='nopull',
            action='store_true',
            help='Skip pulling from origin prior to creation',
            default=False
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
        template_repo = Repository(args.template, nopull=args.nopull)
        template_repo.archive_to(args.ref, args.name)

        if 'box_name' in args and args.box_name:
            box_name = args.box_name
        else:
            box_name = os.path.basename(args.box).strip(".box")

        # for backwards compatibility we provide a mock project object
        class Project(object):
            short_name = args.name

        # build our global context
        template_context = {
            'name': args.name,
            'box_url': args.box,
            'box_name': box_name,

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

        def render_in_place(*parts):
            source = path(*parts)
            data = unicode(open(source).read(), "utf8")
            with open(source, 'w') as f:
                f.write(template.render_string(data))

        # recurse over our template and copy it in into place
        self.log.debug("Copying project template into place...")

        base_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        template_dir = os.path.abspath(os.path.join(base_dir, "..", "project_template"))
        self.log.debug("Processing: {0}".format(template_dir))

        for root, folders, files in os.walk(template_dir):
            relative_dir = root.replace(template_dir, '.')
            self.log.debug(relative_dir)

            for f in files:
                self.log.debug(os.path.join(relative_dir, f))

                shutil.copyfile(os.path.join(root, f), path(relative_dir, f))
                try:
                    render_in_place(relative_dir, f)
                except UnicodeDecodeError:
                    self.log.warn("Failed to render template due to unicode errors: {0}".format(
                        path(relative_dir, f)
                    ))

            for f in folders:
                mkdir(relative_dir, f)

        # read the metadata
        # it must be processed as a template, then loaded as YAML
        self.log.debug("Loading template metadata...")
        metadata = yaml.load(template.render('stackstrap/meta.yml'))

        # move the salt files into place
        if os.path.exists(path('stackstrap', 'state.sls')):
            self.log.debug("Copying template state file to salt/root/%s.sls" % args.name)
            shutil.copyfile(
                path('stackstrap', 'state.sls'),
                path('salt', 'root', '%s.sls' % args.name)
            )
        if os.path.exists(path('stackstrap', 'pillar.sls')):
            self.log.debug("Copying template pillar file to salt/pillar/%s.sls" % args.name)
            shutil.copyfile(
                path('stackstrap', 'pillar.sls'),
                path('salt', 'pillar', '%s.sls' % args.name)
            )

        # iterate the files to parse with Django templates
        self.log.debug("Processing file templates...")
        file_template_paths = metadata.get("file_templates", [])
        file_template_paths.append("stackstrap/meta.yml")
        for p in file_template_paths:
            self.log.debug(p)
            render_in_place(p)

        # iterate the paths to update with custom names
        self.log.debug("Processing path templates...")
        path_templates = metadata.get("path_templates", [])
        for path_template in path_templates:
            for orig_path in path_template:
                self.log.debug("%s -> %s" % (orig_path, path_template[orig_path]))
                os.rename(path(orig_path),
                          path(path_template[orig_path]))

        # now destroy the stackstrap directory as it's no longer needed
        shutil.rmtree(path('stackstrap'), ignore_errors=True)

        self.log.info("Done!\nYou can now 'vagrant up' your development environment from the {name} folder".format(
            name=args.name
        ))
