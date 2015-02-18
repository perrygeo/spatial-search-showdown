#!/usr/bin/env bash
 
sudo apt-get update
 
# install java
sudo apt-get install openjdk-7-jre-headless htop -y
 
# install elasticsearch
wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.4.3.deb
sudo dpkg -i elasticsearch-1.4.3.deb
sudo service elasticsearch start
 
# install head
sudo /usr/share/elasticsearch/bin/plugin --remove mobz/elasticsearch-head
sudo /usr/share/elasticsearch/bin/plugin -install mobz/elasticsearch-head

# Install the river-jdbc plugin
sudo /usr/share/elasticsearch/bin/plugin --remove jdbc
sudo /usr/share/elasticsearch/bin/plugin --install jdbc --url http://xbib.org/repository/org/xbib/elasticsearch/plugin/elasticsearch-river-jdbc/1.4.0.9/elasticsearch-river-jdbc-1.4.0.9-plugin.zip

# Get jar for postgres jdbc driver
sudo wget -O /usr/share/elasticsearch/plugins/jdbc/postgresql-9.4-1200.jdbc41.jar \
 "https://jdbc.postgresql.org/download/postgresql-9.4-1200.jdbc41.jar"

sudo update-rc.d elasticsearch defaults

# copy config template
sudo cp /vagrant/templates/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml

sudo service elasticsearch restart
