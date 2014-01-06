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
available `on the cheeseshop`_. The documentation will install it globally
using ``pip`` but you can certainly install it to a virtualenv if you desire.

Easy Installation
~~~~~~~~~~~~~~~~~
To install StackStrap we're going to be using the ``pip`` script as root so
that StackStrap will be globally available.

.. note:: Linux users may need to install pip
   If you're a Linux user you may need to install a package so that the
   ``pip`` command is available to you. On Debian and it's derivatives
   (Ubuntu, etc) you can install the ``python-pip`` package.

Open up a terminal and run the following command::

    sudo pip install stackstrap

This will install StackStrap and all of it's dependencies. It will place a
command named ``stackstrap`` in your ``$PATH`` so that you can use it from
any where on your system.


.. _Vagrant: http://vagrantup.com/
.. _Vagrant Installation Documention: http://docs.vagrantup.com/v2/installation/index.html
.. _on the cheeseshop: http://pypi.python.org/pypi/stackstrap/
