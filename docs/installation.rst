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

.. _easy_install:

Easy Installation
~~~~~~~~~~~~~~~~~
To install StackStrap we're going to be using the ``easy_install`` command as
root so that StackStrap will be globally available.

Open up a terminal and run the following command::

    sudo easy_install stackstrap

This will install StackStrap and all of it's dependencies. It will place a
command named ``stackstrap`` in your ``$PATH`` so that you can use it from
any where on your system.

The better way - pip
~~~~~~~~~~~~~~~~~~~~
The :ref:`easy_install` method is a very fast way to get up and running with
StackStrap, but using ``easy_install`` is not the best way to install and
manage packages on your system. You should be using ``pip`` to do this. For 
background on why check out this Stack Overflow question: `Why use pip over
easy_install?`_

However, unlike ``easy_install`` you must first install ``pip`` before it can
be used.

Mac OS X
++++++++
On OS X you first need to have the `developer command line tools`_ installed.
Then you need to decide between between two different package managers.

Homebrew_ is a newer package manager that integrates into your base OS X
system libraries and allows for quick & easy installation of packages into a
specific directory, named ``Cellar``, so that it can easily be removed if
necessary.

To get running with Homebrew_:

#. `Install Homebrew`_
#. ``brew install python``
#. ``pip install stackstrap``

`Mac Ports`_ is package manager that has been around for a longer time and does
not integrate with the base OS X system libraries (`the FAQ explains why`_). It
allows for easy installation and use of multiple Python versions (ie. 2.6, 2.7,
3.2 & 3.3).

To get running with `Mac Ports`_ and Python 2.7:

#. `Install Mac Ports`_
#. ``sudo port selfupdate``
#. ``sudo port install py27-pip``
#. ``sudo port select --set pip pip27``
#. ``sudo pip install stackstrap``

.. note:: IMHO
   This section contains the opinions of the developers of StackStrap. These
   are not the only two methods of installing pip on OS X. You can also install
   pip directly to the base OS X system or use Fink. (Plus probably some
   others)

Linux
+++++
If you're on a Linux system your package manage will most likely have a package
for pip ready for you to use.

On Debian based systems::

    sudo apt-get install python-pip

On RedHat based systems with yum::

    sudo yum install python-pip


Windows
+++++++
If you're on a Windows sytem then you'll need to install the setuptools and pip
packages after install python.

See the following StackOverflow question for info: `How to install pip on
windows?`_

.. _Vagrant: http://vagrantup.com/
.. _Vagrant Installation Documentation: http://docs.vagrantup.com/v2/installation/index.html
.. _on the cheeseshop: http://pypi.python.org/pypi/stackstrap/
.. _Why use pip over easy_install?: http://stackoverflow.com/questions/3220404/why-use-pip-over-easy-install
.. _developer command line tools: http://stackoverflow.com/a/9329325
.. _Homebrew: http://brew.sh/
.. _Install Homebrew: https://github.com/Homebrew/homebrew/wiki/Installation
.. _Mac Ports: http://www.macports.org/
.. _the FAQ explains why: http://trac.macports.org/wiki/FAQ#ownlibs
.. _Install Mac Ports: http://www.macports.org/install.php
.. _How to install pip on windows?: http://stackoverflow.com/a/12476379
