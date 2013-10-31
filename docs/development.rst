
Development of StackStrap
-------------------------

You need to have the following software installed on your machine:

* VirtualBox_ (4.3.0 or greater)
* Vagrant_ (1.3.5 or greater)

If this is the first time this vagrant instance will be brought up then you
need to generate your master & minion keys so thatt hey can be preseeded:

.. code-block::
    openssl genrsa -out salt/keys/master.pem 2048
    openssl rsa -in salt/keys/master.pem -pubout > salt/keys/master.pub
    openssl genrsa -out salt/keys/minion.pem 2048
    openssl rsa -in salt/keys/minion.pem -pubout > salt/keys/minion.pub

Once you have done this you can halt and up the vagrant instance all you want.
The keys are marked to be ignored by git so you'll need to do this for each
development instance you setup.

.. _Vagrant: http://vagrantup.com/
.. _VirtualBox: http://virtualbox.org/

.. vim: set ts=4 sw=4 sts=4 et ai :
