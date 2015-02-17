# -*- mode: ruby -*-
# vi: set ft=ruby :
 
Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/trusty64"  
  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    #v.cpus = 2
  end

  config.vm.define "es" do |es|
      es.vm.provision :shell, :path => "install_elasticsearch.sh"
      # es.vm.network :forwarded_port, guest: 9200, host: 9200
      # es.vm.network :forwarded_port, guest: 9300, host: 9300
      es.vm.network "private_network", ip: "192.168.99.3"
  end

  config.vm.define "db" do |db|
      db.vm.provision :shell, :path => "install_postgis.sh"
      # db.vm.network :forwarded_port, guest: 5432, host: 5432
      db.vm.network "private_network", ip: "192.168.99.2"
      db.vm.synced_folder "geonames-for-postgis/work", "/work"
  end

end
