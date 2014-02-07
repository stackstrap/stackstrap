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

Tell me a bit more
------------------
Literally StackStrap is command line tool that parses development stack Templates 
with Jinja and a bit of file management. Keep your Templates in version control 
and constantly add in new best practices.

Moreover, StackStrap is a philosophy geared towards helping teams with many different 
points of view and skills sets work together efficiently in short time frames. System 
management is all rolled in because of the power of Salt. This means that development 
environments are always tailored to the current branch. It is also very keen on 
automation, with the idea that someone just helping integrate some cool CSS transforms 
can be ready to run as well.

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
