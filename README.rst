StackStrap
==========

An awesome tool that uses vagrant + salt to make development suck less.

Overview
--------

Let's face it, writing code is awesome, but writing code in a team without
a great strategy and a solid devops team supporting you it can get really
frustrating.

Vagrant_ does an amazing job or automating the task of bringing up virtual
machines for development, but it doesn't do too much in the way of configuring
the operating system. Enter it's provisioners_, these allow you the ability
to configure the system after Vagrant creates it but knowing how you should be
configuring the system is a whole other question.

StackStrap aims to ease this situation by utilizing the Salt_ provisioner in
Vagrant along with a `community repository` of Salt_ states combined with an
easy to use web interface, built using Django, that allows you to quickly and
reliably create development environments (and in the future provision your
production servers too).

Template Metadata Format
------------------------
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

Development of StackStrap
-------------------------

You need to have the following software installed on your machine:

* VirtualBox_ (4.3.0 or greater)
* Vagrant_ (1.3.5 or greater)

If this is the first time this vagrant instance will be brought up then you
need to generate your master & minion keys so thatt hey can be preseeded:

.. code-block::
    openssl genrsa -out salt/keys/master.pem 2048
    openssl rsa -in salt/keys/master.pem -pubout > salt/keys/master.pub
    openssl genrsa -out salt/keys/minion.pem 2048
    openssl rsa -in salt/keys/minion.pem -pubout > salt/keys/minion.pub

Once you have done this you can halt and up the vagrant instance all you want.
The keys are marked to be ignored by git so you'll need to do this for each
development instance you setup.

.. _VirtualBox: http://virtualbox.org/
.. _Vagrant: http://vagrantup.com/
.. _Salt: http://saltstack.com/
.. _provisioners: http://docs.vagrantup.com/v2/provisioning/index.html
.. _community repository: https://github.com/fatbox/stackstrap-salt
.. _Django's template system: https://docs.djangoproject.com/en/dev/ref/templates/


.. vim: set ts=4 sw=4 sts=4 et ai :
