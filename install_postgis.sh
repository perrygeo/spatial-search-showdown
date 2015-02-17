#!/usr/bin/env bash
 
# sudo apt-get update
# sudo apt-get upgrade -yy

sudo apt-get install -y postgresql postgresql-contrib postgis postgresql-9.3-postgis-2.1 htop

# copy templates
sudo cp /vagrant/templates/postgresql.conf /etc/postgresql/9.3/main/postgresql.conf
sudo cp /vagrant/templates/pg_hba.conf /etc/postgresql/9.3/main/pg_hba.conf

sudo service postgresql restart

sudo -u postgres psql -c "DROP DATABASE IF EXISTS geonames;"
sudo -u postgres psql -c "CREATE USER vagrant WITH PASSWORD 'vagrant';"
sudo -u postgres psql -c "CREATE DATABASE geonames;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE geonames to vagrant;" 
sudo -u postgres psql -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;" geonames
