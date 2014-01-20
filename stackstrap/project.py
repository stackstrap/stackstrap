import inspect
import logging
import errno
import os
import shutil
import yaml

from stackstrap.jinja import JinjaInterface


class ProjectException(Exception):
    pass


class Project(object):
    def __init__(self, name):
        self.log = logging.getLogger("project")

        self.name = name

        # for backwards compatibility
        self.short_name = self.name

    def create(self, template):
        if os.path.exists(self.name):
            raise ProjectException(
                "The specified name '{name}' already exists".format(
                    name=self.name
                ))

        if not template.validated:
            template.validate()

        self.log.info(
            "Creating a new project named '{name}' \
            using {template} as the template...".format(
            name=self.name,
            template=template.name
        ))

        # copy our template to the new project name
        template.copy_to(self.name)

        # build our global context
        render_context = {
            'name': self.name,

            # for backwards compatibility
            'project': self,
            'template': template,
        }

        # create our jinja template interface
        jinja = JinjaInterface(
            globals=render_context,
            file_loader_paths=[os.path.abspath(self.name)]
        )

        def path(*parts):
            return os.path.abspath(os.path.join(self.name, *parts))

        def render_in_place(*parts):
            source = path(*parts)
            data = unicode(open(source).read(), "utf8")
            with open(source, 'w') as f:
                f.write(jinja.render_string(data))

        # read the metadata
        # it must be processed as a template, then loaded as YAML
        self.log.debug("Loading template metadata...")
        metadata = yaml.load(jinja.render_file('stackstrap.yml'))

        # iterate through the cleanup paths
        self.log.debug("Processing cleanup...")
        cleanup_paths = metadata.get("cleanup", [])
        for p in cleanup_paths:
            self.log.debug(p)
            cleanup_path = path(p)
            if os.path.isdir(cleanup_path):
                shutil.rmtree(cleanup_path)
            elif os.path.exists(cleanup_path):
                os.remove(cleanup_path)
            else:
                self.log.error("Unable to cleanup: %s" % cleanup_path)

        # iterate the files to parse with Jinja templates
        self.log.debug("Processing file templates...")
        file_template_paths = metadata.get("file_templates", [])
        file_template_paths.append("stackstrap.yml")
        for p in file_template_paths:
            self.log.debug(p)
            render_in_place(p)

        # iterate the paths to update with custom names
        self.log.debug("Processing path templates...")
        path_templates = metadata.get("path_templates", [])
        for path_template in path_templates:
            for orig_path in path_template:
                self.log.debug(
                    "%s -> %s" % (orig_path, path_template[orig_path])
                )
                os.rename(path(orig_path),
                          path(path_template[orig_path]))

        # now destroy the stackstrap.yml file as it's no longer needed
        os.unlink(path('stackstrap.yml'))

        self.log.info("Done! The project {name} has been created".format(
            name=self.name
        ))
