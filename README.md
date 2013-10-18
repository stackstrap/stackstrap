StackStrap
==========

An awesome tool that uses vagrant + salt to make development suck less.

Overview
--------

StackStrap is a Django based web application

Development of StackStrap
-------------------------

You need to have the following software installed on your machine:

* [Vagrant](http://vagrantup.com)
* [VirtualBox](http://virtualbox.org)
* [Salty Vagrant](https://github.com/saltstack/salty-vagrant/)

At the time of writing the salty vagrant plugin (0.4.0) does not correctly work
for our needs. Instead you need to [install from source](https://github.com/saltstack/salty-vagrant#installing-from-source).

If this is the first time this vagrant instance will be brought up then you
need to generate your master & minion keys so thatt hey can be preseeded:

    openssl genrsa -out salt/keys/master.pem 2048
    openssl rsa -in salt/keys/master.pem -pubout > salt/keys/master.pub
    openssl genrsa -out salt/keys/minion.pem 2048
    openssl rsa -in salt/keys/minion.pem -pubout > salt/keys/minion.pub

Once you have done this you can halt and up the vagrant instance all you want.
The keys are marked to be ignored by git so you'll need to do this for each
development instance you setup.
