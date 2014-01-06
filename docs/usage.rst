Using StackStrap
================
Once StackStrap has been installed you'll have the ``stackstrap`` command
available to you in the terminal. You'll use this command to create new
projects from a :ref:`template repository <template>`.

Adding a template
-----------------
To add a template use the ``stackstrap template add`` command and provide it
a name along with the GIT URL of a StackStrap template::

   stackstrap template add django https://github.com/fatbox/stackstrap-django.git

Creating a new project
----------------------
To create a project use the ``stackstrap create`` command and provide it a
project name and the name of an available template::

   stackstrap create myproject django

Command line help
-----------------
The ``stackstrap`` command has built in documentation, run it with the ``-h``
or ``--help`` flag for more information on the options you can set from the
command line.

You can also get help about a specific command by passing it help::

    stackstrap create --help
