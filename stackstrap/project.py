import inspect
import logging
import os
import shutil
import yaml

from stackstrap.jinja import JinjaInterface

class Project(object):
    def __init__(self, name, template):
        self.log = logging.getLogger("project")

        self.name = name
        self.template = template

        # for backwards compatibility
        self.short_name = self.name

    def create(self):
        if os.path.exists(self.name):
            self.log.error("The specified name '{name}' already exists".format(
                name=self.name
            ))
            return False

        if not self.template.validated:
            self.template.validate()

        if not self.template.repository:
            self.log.error("Failed to setup template repository. Cannot create a new project")
            return

        self.log.info("Creating a new project named '{name}' using {template} as the template...".format(
            name=self.name,
            template=self.template.name
        ))

        # access the repository and archive it to our destination project name
        self.template.archive_to(self.name)

        # build our global context
        render_context = {
            'name': self.name,
            'box_url': self.template.box,
            'box_name': self.template.box_name,

            # for backwards compatibility
            'project': self,
            'template': self.template,
        }

        # create our jinja template interface
        jinja = JinjaInterface(
            globals=render_context,
            file_loader_paths=[os.path.abspath(self.name)]
        )

        def mkdir(*parts):
            return os.mkdir(os.path.join(self.name, *parts), 0755)

        def path(*parts):
            return os.path.join(self.name, *parts)

        def render_in_place(*parts):
            source = path(*parts)
            data = unicode(open(source).read(), "utf8")
            with open(source, 'w') as f:
                f.write(jinja.render_string(data))

        # recurse over our template and copy it in into place
        self.log.debug("Copying project template into place...")

        base_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        template_dir = os.path.abspath(os.path.join(base_dir, "project_template"))
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
        metadata = yaml.load(jinja.render_file('stackstrap/meta.yml'))

        # move the salt files into place
        if os.path.exists(path('stackstrap', 'state.sls')):
            self.log.debug("Copying template state file to salt/root/%s.sls" % self.name)
            shutil.copyfile(
                path('stackstrap', 'state.sls'),
                path('salt', 'root', '%s.sls' % self.name)
            )
        if os.path.exists(path('stackstrap', 'pillar.sls')):
            self.log.debug("Copying template pillar file to salt/pillar/%s.sls" % self.name)
            shutil.copyfile(
                path('stackstrap', 'pillar.sls'),
                path('salt', 'pillar', '%s.sls' % self.name)
            )

        # iterate the files to parse with Jinja templates
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
            name=self.name
        ))
