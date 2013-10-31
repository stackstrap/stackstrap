Templates
=========

Inside of template repositories you can create a special file name named
`stackstrap` that contains metadata informing the template system of which
files need to be parsed as templates and which directories need to be renamed.

.. code-block:: yaml
    ---
    stackstrap:
      path_templates:
        'project_app/something/else': 'project_app/something/{{ project.id }}'
        'project_app': '{{ project.name }}_app'

      file_templates:
        - deployment/deploy.rb

The `path_templates` entries define paths that should be transformed based on
the current context. They are evaluated in the order that they are defined and
are relative to the root of the template. The example above shows how you would
process a nested directory first and then its parent directory second.

The `file_templates` entries define files, again relative to the root of the
template, which should be parsed using `Django's template system` before they
are sent to the user.

When both path & file templates are parsed they are provided a context that
contains the following items to use:

* `project` -- the current project object
* `membership` -- the membership to the project, from here you can get the
                  current user and any related attributes

.. _Django's template system: https://docs.djangoproject.com/en/dev/ref/templates/

.. vim: set ts=4 sw=4 sts=4 et ai :
