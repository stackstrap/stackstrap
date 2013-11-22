StackStrap documentation
========================

An awesome tool that uses vagrant + salt to make development suck less.

Overview
--------

Let's face it, writing code is awesome, but writing code in a team without
a great strategy and a solid devops team supporting you can get really
frustrating when trying to manage development environments within the
team. 

Vagrant_ does an amazing job or automating the task of bringing up virtual
machines for development, but it doesn't do too much in the way of configuring
the operating system. Enter it's provisioners_, these allow you the ability
to configure the system after Vagrant creates it but knowing how you should be
configuring the system is a whole other question.

StackStrap aims to ease this situation by utilizing the Salt_ provisioner in
Vagrant along with a `community repository`_ of Salt_ states combined with an
easy to use web interface, built using Django, that allows you to quickly and
reliably create development environments (and in the future provision your
production servers too).

Here be dragons
---------------
StackStrap is currently **alpha** quality software and is undergoing rapid
change. The interface, salt integration, template format and all other pieces
of the system are in flux and may change at any time without notice.

Getting Help
------------
You can find us in #stackstrap on freenode if you want to chat or need help.

There is also a `Google Group`_ (stackstrap@googlegroups.com).

Contents
--------

.. toctree::
   :maxdepth: 2

   conventions.rst
   deployment.rst
   templates.rst
   development.rst
   usage.rst

.. _Vagrant: http://vagrantup.com/
.. _Salt: http://saltstack.com/
.. _provisioners: http://docs.vagrantup.com/v2/provisioning/index.html
.. _community repository: https://github.com/fatbox/stackstrap-salt
.. _Google Group: https://groups.google.com/d/forum/stackstrap
