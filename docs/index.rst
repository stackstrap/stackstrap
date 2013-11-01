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

Contents:

.. toctree::
   :maxdepth: 2

   deployment.rst
   templates.rst
   development.rst

.. _Vagrant: http://vagrantup.com/
.. _Salt: http://saltstack.com/
.. _provisioners: http://docs.vagrantup.com/v2/provisioning/index.html
.. _community repository: https://github.com/fatbox/stackstrap-salt
