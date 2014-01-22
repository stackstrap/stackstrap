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

.. code::

    sudo easy_install stackstrap

Add a Template:

.. code::

    stackstrap template add django https://github.com/freesurface/stackstrap-django.git

Create a new Project:

.. code::

    stackstrap create mynewproject django

Change into the new folder:

.. code::

    cd mynewproject

Vagrant Up:

.. code::

    vagrant up

Documentation
-------------
Full documentation can be found at RTD: http://stackstrap.readthedocs.org

The source for the documentation is in the `docs` directory.


.. _Salt: http://saltstack.org/
.. _Vagrant: http://vagrantup.com/
.. _community repository of Salt states: http://github.com/freesurface/stackstrap-salt/

Salted Boxes
------------

Ubuntu 12.04
++++++++++++

32 bit:

.. code::

    http://boxes.stackstrap.org/virtualbox/ubuntu1204-i386-saltlatest.box

64 bit:

.. code::

    http://boxes.stackstrap.org/virtualbox/ubuntu1204-saltlatest.box

Debian 7.3
++++++++++

32 bit:

.. code::

    http://boxes.stackstrap.org/virtualbox/debian73-i386-saltlatest.box

64 bit:

.. code::

    http://boxes.stackstrap.org/virtualbox/debian73-saltlatest.box

CentOS 6.5
++++++++++

32 bit:

.. code::

    http://boxes.stackstrap.org/virtualbox/centos65-i386-saltlatest.box

64 bit:

.. code::

    http://boxes.stackstrap.org/virtualbox/centos65-saltlatest.box

Fedora 20
+++++++++

32 bit:

.. code::

    http://boxes.stackstrap.org/virtualbox/fedora20-i386-saltlatest.box

64 bit:

.. code::

    http://boxes.stackstrap.org/virtualbox/fedora20-saltlatest.box

.. vim: set ts=4 sw=4 sts=4 et ai :
