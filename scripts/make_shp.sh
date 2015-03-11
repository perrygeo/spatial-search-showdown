export pg='dbname=geonames host=geonames.db port=5432 user=postgres'

ogr2ogr -f SQLite -dsco SPATIALITE=YES geonames.sqlite PG:"$pg" geoname
