Installing StackStrap
=====================
StackStrap is a command line tool written in Python. It will install on any
Mac OS X or Linux computer. Windows usage is definitely possible but has not
been documented yet.

Installing Vagrant
------------------
Since StackStrap uses Vagrant_ for the management of the virtual machine images
that will be used for development you will need to have Vagrant_ installed on
your workstation. See the `Vagrant Installation Documentation`_ for
instructions.

Installing StackStrap
---------------------
It's very easy to install StackStrap as it's a standard Python package that's
available `on the cheeseshop`_.

The documentation will install it globally using ``easy_install`` but you can 
certainly install it using ``pip`` to a virtualenv if you desire.

Easy Installation
~~~~~~~~~~~~~~~~~
To install StackStrap we're going to be using the ``easy_install`` command as
root so that StackStrap will be globally available.

Open up a terminal and run the following command::

    sudo easy_install stackstrap

This will install StackStrap and all of it's dependencies. It will place a
command named ``stackstrap`` in your ``$PATH`` so that you can use it from
any where on your system.


.. _Vagrant: http://vagrantup.com/
.. _Vagrant Installation Documentation: http://docs.vagrantup.com/v2/installation/index.html
.. _on the cheeseshop: http://pypi.python.org/pypi/stackstrap/
