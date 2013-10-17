# -*- mode: ruby -*-
# vim: set ft=ruby ts=2 sw=2 et sts=2 :
#
# Vagrant file for StackStrap 
#

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.hostname = "stackstrap-master.local"

  config.vm.box = "precise32"
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

  config.vm.network :public_network
  config.ssh.forward_agent = true

  config.vm.synced_folder "application", "/application"
  config.vm.synced_folder "salt/roots", "/srv"

  config.vm.provision :salt do |salt|
    salt.minion_config = "salt/minion"
    salt.master_config = "salt/master"

    salt.install_type = "stable"
    salt.install_master = true

    salt.seed_master = {
      :'stackstrap-master' => 'salt/stackstrap-master.pub'
    }

    salt.run_highstate = true

    salt.verbose = true
  end
end
