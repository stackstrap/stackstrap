Documentation conventions
=========================

Shell Commands
--------------
Anytime a command line example is given it will be shown as a literal block of
text and will be prefixed by either a hash-sign (``#``) for commands to be run
as root or a dollar-sign (``$``) for commands to be run as the stackstrap user.

Example root command::

    # cp -f /home/stackstrap/current/salt/{master,minion} /etc/salt/

Example user command::

    $ git clone https://github.com/fatbox/stackstrap.git initial
