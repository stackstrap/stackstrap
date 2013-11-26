Deploying the StackStrap Master
===============================
The StackStrap Master can be deployed on any UNIX like host capable of running
nginx, python 2.7 and uwsgi. Currently it is supported best on Debian Linux
and its derivatives (Ubuntu, etc).

Like all systems managed by the master, it itself is configured by itself so
deployment is a fairly straight forward task.

#. Install the base OS, pick a hostname that starts with ``stackstrap-master``,
   ie. ``stackstrap-master.yourdomain.com``. The hostname should also resolve
   without the domain name, ie. ``ping stackstrap-master`` works
#. Install salt using the `salt-bootstrap`_ script. Specify ``-M`` to install
   the master::

    # wget --no-check-certificate -O bootstrap.sh http://bootstrap.saltstack.org
    # sh bootstrap.sh -M

#. Create the stackstrap group & user::

    # groupadd -g 6000 stackstrap
    # useradd -d /home/stackstrap -m -s /bin/sh -u 6000 -g 6000 stackstrap

#. To allow salt to do most of the work we need to manually create a release
   for stackstrap so we can use its salt states::

    # apt-get install git
    # su - stackstrap
    $ mkdir releases
    $ cd releases
    $ git clone https://github.com/fatbox/stackstrap.git initial
    $ cd initial
    $ git submodule init
    $ git submodule update
    $ cd ~
    $ ln -s releases/initial current

#. Copy the salt config into place::

    # cp -f /home/stackstrap/current/salt/{master,minion} /etc/salt/
    # service salt-master restart
    # service salt-minion restart

#. Make sure the key is accepted. Replace the hostname below with your FQDN::

    # salt-key -ya stackstrap-master.fatbox.ca

#. Set the master to be in production mode. See `Creating a configuration`_
   below.

#. Let salt configure everything else you'll need::

    # salt-call state.highstate

#. Create the Django database and initial admin user::

    # su - stackstrap
    $ source virtualenv/bin/activate
    $ export PYTHONPATH=/home/stackstrap/current/application/stackstrap
    $ export DJANGO_SETTINGS_MODULE=stackstrap.settings.prod
    $ django-admin.py syncdb
    $ supervisorctl start stackstrap

#. Profit

Creating a configuration
------------------------
The StackStrap Master is configured through the salt grains system. By default
the master is configured for dev mode.

Create a file named: ``/etc/salt/minion.d/stackstrap.conf``

Configure the grains under the ``stackstrap`` namespace. The following is a
minimal example that puts the master into production mode with all the other
settings as their defaults::

    grains:
      stackstrap:
        mode: 'prod'

Any time this configuration is updated you should re-apply the state via salt
to ensure the system is configured correctly::

    # salt-call state.highstate

Available configuration items
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**mode** - This can be set to ``dev`` or ``prod``. By default it is ``dev``.
This affects how the master application is run. In ``dev`` mode it runs the
Django built-in server (``runserver``) and in ``prod`` mode it runs the
application under uwsgi behind nginx.

**http_server_name** - The name to apply to the nginx ``server`` block. By
default it is ``_`` (match any name supplied).

**http_ssl** - Can be set to ``True`` to have the nginx ``server`` block
be an SSL enabled block. An equivalent ``server`` will be setup on port 80 and
will redirect all traffic to the SSL port.

**http_ssl_certificate** - The path to the certificate file to be used by
nginx in SSL mode.

**http_ssl_certificate_key** - The path to the key file to be used by nginx
in SSL mode.


.. _salt-bootstrap: https://github.com/saltstack/salt-bootstrap
