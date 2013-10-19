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

Development of StackStrap
-------------------------

You need to have the following software installed on your machine:

* VirtualBox_ (4.3.0 or greater)
* Vagrant_ (1.3.5 or greater)

If this is the first time this vagrant instance will be brought up then you
need to generate your master & minion keys so thatt hey can be preseeded:

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
