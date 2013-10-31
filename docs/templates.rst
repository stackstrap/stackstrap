Project Templates
=================

Project Templates are GIT repositories that contain a base layout for a project
and are coupled with pillar & state data that Salt uses to provision the
project.

The files inside the template can be parsed as Django templates, by marking
them to be parsed in the meta-data, if you need any of your files to be 
updated (which you pretty much always do).

You can also apply the same template logic to path names so that you can apply
transformations to the filesystem to ensure that best practicies for naming
and consistency are applied.

The fact that we have Project Templates and Django has a template engine that
we use for files can become confusing. To help with the confusion we will
always refer to our Project Templates with uppercase letters and to Django
templates with a lowercase 't'.

Project Template meta-data
--------------------------
The meta-data for Project Templates is supplied as pillar & state data and
describes the Project Template, which files should be treated as Django
templates, which directories to transform and how state should be applied to
systems using the Project Template.

The pillar data needs to specify some basic information about your Project
Template but can be used to store any data you want to use in your states. The
pillar data is passed through the Django template engine prior to being used,
which is how the path_templates work for the filesystem transforms, so you can
use any of the available context variables when defining your pillar data.

The state data should utilize the available states and macros that can be
found in the `community repository`_.

The meta-data should live in a directory named ``stackstrap``. The pillar data
should live in a file named ``pillar.sls`` and the state data should live in a
file named ``state.sls``.

Base pillar data
~~~~~~~~~~~~~~~~
The pillar data should live inside a file named ``stackstrap/pillar.sls`` and
should define a top-level name space of ``stackstrap`` with a minimum of the
following fields:

* **`template_name`** - a short name to describe the Project Template
* **`template_author`** - your name (formatted as "Full Name <email@address>")
* **`template_description`** - a longer multi-line description of the Project Template

Example::

    stackstrap:
      template_name: "Flask with Capistrano (nginx + uwsgi)"
      template_author: "Brent Smyth <brent@fatbox.ca>"
      template_description:
        This template contains a Flask app with Flask Script for managing it.

        It is deployed using nginx as the HTTP endpoint and uwsgi as the
        application server.

Parsing files as Django templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To tell StackStrap that a file should be passed through the Django template
engine when creating a project instance you need to define a list named
``file_templates`` inside the ``stackstrap`` name space containing the file
paths relative to the root of the project::

    stackstrap:
      file_templates:
        - .ruby-gemset
        - deployment/deploy.rb
        - deployment/js_compress.json
        - foundation/config.rb

Transforming filesystem paths
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To tell StackStrap that filesystem paths should be transformed based on the
context data when creating a project instance you need to define a dictionary
named ``path_templates`` inside the ``stackstrap`` name space containing the
original path name as the key and the transformed path name, using the
available context variables, as the value::

    stackstrap:
      path_templates:
        'project_app/something/else': 'project_app/something/{{ project.id }}'
        'project_app': '{{ project.slug }}_app'

Filesystem paths are transformed in the order they are listed, so list your
more specific matches first as in the example above. Also, the filesystem
transforms are applied after the ``file_templates`` (above) so if you're
specifying a file to both be treated as a template and have its filesystem
path transformed specify the original path name in the ``file_templates``
list and not the transformed one.

Available context variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~
When the pillar data and your templates are parsed the following variables are
made available in the context:

* **`project`** - the Project object. See the `Project source code` for all of
  the available attributes you can access on this object.
* **`membership`** - the Membership object linking the user that is deploying
  the code with the project. You can get at the user object via
  ``membership.user``


.. _Django's template system: https://docs.djangoproject.com/en/dev/ref/templates/
.. _community repository: https://github.com/fatbox/stackstrap-salt
.. _Project source code: https://github.com/fatbox/stackstrap/blob/master/application/stackstrap/projects/models.py

.. vim: set ts=4 sw=4 sts=4 et ai :
