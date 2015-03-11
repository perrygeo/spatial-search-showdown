#!/bin/bash
echo "Backing up geonames..."
pg_dump -Fc -U postgres -h localhost geonames > geonames.postgis.dump

echo <<EOT
To restore,
    dropdb geonames
    createdb -T template0 geonames
    pg_restore -d geonames geonames.postgis.dump
EOT
