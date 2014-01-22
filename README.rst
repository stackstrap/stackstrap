StackStrap
==========
Making development more awesome by combining the power of Salt_ and Vagrant_
with templates and a macro driven `community repository of Salt states`_.

.. image:: https://api.travis-ci.org/freesurface/stackstrap.png?branch=master
           :target: https://travis-ci.org/freesurface/stackstrap

.. image:: https://coveralls.io/repos/freesurface/stackstrap/badge.png
           :target: https://coveralls.io/r/freesurface/stackstrap

.. image:: https://pypip.in/v/stackstrap/badge.png
           :target: https://crate.io/packages/stackstrap/
           :alt: Latest PyPI version

.. image:: https://pypip.in/d/stackstrap/badge.png
           :target: https://crate.io/packages/stackstrap/
           :alt: Number of PyPI downloads

Getting Started
---------------

Install:

.. code:: console

    sudo easy_install stackstrap

Add a Template:

.. code:: console

    stackstrap template add django https://github.com/freesurface/stackstrap-django.git

Create a new Project:

.. code:: console

    stackstrap create mynewproject django

Change into the new folder:

.. code:: console

    cd mynewproject

Vagrant Up:

.. code:: console

    vagrant up

Documentation
-------------
Full documentation can be found at RTD: http://stackstrap.readthedocs.org

The source for the documentation is in the `docs` directory.


.. _Salt: http://saltstack.org/
.. _Vagrant: http://vagrantup.com/
.. _community repository of Salt states: http://github.com/freesurface/stackstrap-salt/

.. vim: set ts=4 sw=4 sts=4 et ai :
