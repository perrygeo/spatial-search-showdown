from flask import Flask, jsonify, request
import os
import sqlalchemy
from sqlalchemy.sql import text
import json
import requests

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
        # provider = "postgis"
        provider = "elasticsearch"
    bbox = [float(x) for x in bbox_str.split(',')]
    bounds = dict(zip(['west','south','east','north'], bbox))

    if provider == "postgis":
        results = query_postgis(bounds)
    elif provider == "elasticsearch":
        results = query_elasticsearch(bounds)

    return jsonify(results)


def query_postgis(bounds):
    result = conn.execute(sqltext, **bounds)
    features = []
    for row in result:
        f = {
          'type': 'Feature',
          'geometry': json.loads(row['geometry']),
          'properties': {
              'name': row['name'],
              'featuretype': row['featuretype'],
              'alt': row['alternatenames']
          }
        }
        features.append(f)
    return {
        'type': 'FeatureCollection',
        'features': features
    }


def query_elasticsearch(bounds):
    page_size = 1000

    query = {
        "from" : 0, 
        "size" : page_size,
        "query": {
            "filtered" : {
                "query" : {
                    "match_all" : {}
                },
                "filter" : {
                    "geo_bounding_box" : {
                        "location" : {
                            "top" : float(bounds['north']),
                            "left" : float(bounds['west']),
                            "bottom" : float(bounds['south']),
                            "right" : float(bounds['east']) 
                        }
                    }
                }
            }
        }
    }
    query_str = json.dumps(query)
    req = session.get(URL, data=query_str) 

    features = []
    for hit in req.json()['hits']['hits']: # TODO error checking? 
        data = hit['_source']
        f = {
            'type': 'Feature',
            'geometry': {
                "coordinates": [
                    data['location']['lon'],
                    data['location']['lat']],
                "type": "Point"
            },
            'properties': {
              'name': data['name'],
              'featuretype': data['featuretype'],
              'alt': data['alternatenames']
            }
        }
        features.append(f)

    return {
        'type': 'FeatureCollection',
        'features': features
    }


if __name__ == '__main__':
    app.run(debug=True)
