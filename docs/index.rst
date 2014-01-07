StackStrap documentation
========================

A tool that uses vagrant + salt to make development more awesome.

Overview
--------

Let's face it, writing code is awesome, but writing code in a team without
a great strategy and a solid devops team supporting you can get really
frustrating when trying to manage development environments within the
team. 

Vagrant_ does an amazing job of automating the task of bringing up virtual
machines for development, but it doesn't do too much in the way of configuring
the operating system. Enter it's provisioners_, these allow you the ability
to configure the system after Vagrant creates it but knowing how you should be
configuring the system is a whole other question.

StackStrap aims to ease this situation by utilizing the Salt_ provisioner in
Vagrant along with a `community repository`_ of Salt_ states that allow you to
quickly and reliably create development environments using our simple macros.

Here be dragons
---------------
StackStrap is currently **alpha** quality software and is undergoing rapid
change. The interface, salt integration, template format and all other pieces
of the system are in flux and may change at any time without notice.

January 1st, 2014: New year, new approach. We've done a complete 180 degree
turn on the approach for how stackstrap works. If you used it prior to Jan 1
2014 please make sure to read the docs again to familiarize yourself with the
changes. They are drastic.

Getting Help
------------
You can find us in #stackstrap on freenode if you want to chat or need help.

There is also a `Google Group`_ (stackstrap@googlegroups.com).

Contents
--------

.. toctree::
   :maxdepth: 2

   installation.rst
   usage.rst
   templates.rst

.. _Vagrant: http://vagrantup.com/
.. _Salt: http://saltstack.com/
.. _provisioners: http://docs.vagrantup.com/v2/provisioning/index.html
.. _community repository: https://github.com/openops/stackstrap-salt
.. _Google Group: https://groups.google.com/d/forum/stackstrap
