from flask import Flask, jsonify, request
import os
import sqlalchemy
from sqlalchemy.sql import text
import json
import requests
from providers import postgis, elasticsearch

app = Flask(__name__)

# Postgres connections
db = sqlalchemy.create_engine('postgresql+psycopg2://postgres:@192.168.99.2/geonames')
conn = db.connect()
sql = text("""
SELECT
    g.name,
    g.alternatenames,
    f.name as featuretype,
    ST_AsGeoJSON(g.the_geom) AS geometry
FROM geoname AS g
JOIN featurecodes AS f
ON f.code = g.featurecodeid
WHERE g.the_geom && ST_MakeEnvelope(:west, :south, :east, :north, 4326)
""")


# HTTP Sessions, for elasticsearch
session = requests.Session()
URL = "http://192.168.99.3:9200/geonameidx/_search"


@app.route('/')
def main():
    return app.send_static_file('index.html')


@app.route('/geonames/search')
def geonames():
    bbox_str = request.args.get('bbox')
    provider = request.args.get('provider')
    if not provider:
        # default provider
        provider = "postgis"
        #provider = "elasticsearch"
    bbox = [float(x) for x in bbox_str.split(',')]
    bounds = dict(zip(['west','south','east','north'], bbox))

    if provider == "postgis":
        results = postgis(bounds, conn, sql)
    elif provider == "elasticsearch":
        results = elasticsearch(bounds, session, URL)

    return jsonify(results)
    

if __name__ == '__main__':
    app.run(debug=True)
