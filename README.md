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

If this is the first run then it will bail out because you need to preseed
the minion key in salty vagrant. The first step is to create an empty key file
for the purpose of getting salt installed:

  touch salt/stackstrap-master.pub

Then bring up the development server:

   vagrant up

This will install salt and then fail with an error "Minion did not return" when
it tries to apply the high state. Next login to the server and get the correct
public key contents:

    vagrant ssh
    sudo cat /etc/salt/pki/minion/minion.pub
    exit

Now put the contents of the minion's public key into the file you touched,
salt/stackstrap-master.pub, and then re-provision with vagrant:

    vagrant provision


This pull is crucial: https://github.com/mitchellh/vagrant/pull/2359
