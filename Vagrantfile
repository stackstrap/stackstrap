# -*- mode: ruby -*-
# vim: set ft=ruby ts=2 sw=2 et sts=2 :
#
# Vagrant file for StackStrap 
#

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.hostname = "stackstrap-master"

  config.vm.box = "precise32"
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

  config.vm.network :public_network

  # we share our application folder with uid/gid 6000
  # this is the value our salt states will create for the
  # stackstrap user
  config.vm.synced_folder "application", "/application",
    :mount_options => ["uid=6000,gid=6000"]
    #owner: 6000, group: 6000 # XXX TODO https://github.com/mitchellh/vagrant/pull/2390

  # since we're the salt master we need our salt roots shared
  # stackstrap clients do not need to specify a salt synced folder
  config.vm.synced_folder "salt/roots", "/srv"

  config.ssh.forward_agent = true

  # provision our box with salt
  config.vm.provision :salt do |salt|
    salt.verbose = true
    salt.install_type = "stable"
    salt.install_master = true

    salt.minion_config = "salt/minion"
    salt.minion_key = "salt/keys/minion.pem"
    salt.minion_pub = "salt/keys/minion.pub"

    salt.master_config = "salt/master"
    salt.master_key = "salt/keys/master.pem"
    salt.master_pub = "salt/keys/master.pub"

    salt.seed_master = {
      :'stackstrap-master' => salt.minion_pub
    }

    salt.run_highstate = true

    # this lists all of our default pillar data
    salt.pillar({
      'stackstrap' => {
        # mode: dev|prod
        # in dev mode we run nginx in proxy mode with runserver behind it
        # in prod mode we run nginx + uwsgi
        'mode' => 'dev',

        # the hostname to use when configuring nginx
        'http_server_name' => '_',

        # the port to listen on
        'http_listen' => '80',

        # the interface on which to connect to our master
        # this is setup to be eth1 by default so that it works on our virtualbox
        # guest images, you'll want to change it in production
        'master_interface' => 'eth1'
      }
    })
  end
end
