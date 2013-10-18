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
  config.ssh.forward_agent = true

  # we share our application folder with uid/gid 6000
  # this is the value our salt states will create for the
  # stackstrap user
  config.vm.synced_folder "application", "/application",
    owner: 6000, group: 6000

  config.vm.synced_folder "salt/roots", "/srv"

  config.vm.provision :salt do |salt|
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
  end
end
