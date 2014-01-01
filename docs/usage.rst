Using StackStrap
================
Once StackStrap has been installed you'll have the ``stackstrap`` command
available to you in the terminal. You'll use this command to create new
projects from a :ref:`template repository <template>`.

Creating a new project
----------------------
To create a project use the ``stackstrap create`` command and provide it a
project name and the GIT URL of the template you wish to use::

   stackstrap create myproject https://github.com/fatbox/stackstrap-django.git

Command line help
-----------------
The ``stackstrap`` command has built in documentation, run it with the ``-h``
or ``--help`` flag for more information on the options you can set from the
command line.

You can also get help about a specific command by passing it help::

    stackstrap create --help
