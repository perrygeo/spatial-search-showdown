from flask import Flask, jsonify, request
import os
import sqlalchemy
from sqlalchemy.sql import text
import json
import requests

db = sqlalchemy.create_engine('postgresql+psycopg2://postgres:@192.168.99.2/geonames')
conn = db.connect()
app = Flask(__name__)

session = requests.Session()

sqltext = text("""SELECT 
     g.name,
     g.alternatenames,
     f.name as featuretype,
     ST_AsGeoJSON(g.the_geom) AS geometry
FROM geoname AS g
JOIN featurecodes AS f
ON f.code = g.featurecodeid
WHERE g.the_geom && ST_MakeEnvelope(:west, :south, :east, :north, 4326)
""")


@app.route('/')
def main():
    return app.send_static_file('index.html')

    return '''
    <ul>
    <li>
        <a href="/postgis/search?bbox=10.9351,49.3866,11.201,49.5138">
          /postgis/search?bbox=10.9351,49.3866,11.201,49.5138
        </a>
    </li>
    <li>
        <a href="/elasticsearch/search?bbox=10.9351,49.3866,11.201,49.5138">
          /elasticsearch/search?bbox=10.9351,49.3866,11.201,49.5138
        </a>
    </li>
    </ul>
'''

@app.route('/postgis/search')
def postgis():
    bbox_str = request.args.get('bbox')
    bbox = [float(x) for x in bbox_str.split(',')]
    bounds = dict(zip(['west','south','east','north'], bbox))

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

    return jsonify({
        'type': 'FeatureCollection',
        'features': features
    })

PAGE_SIZE=1000
URL="http://192.168.99.3:9200/geonameidx/_search"

@app.route('/elasticsearch/search')
def elasticsearch():
    bbox_str = request.args.get('bbox')
    bbox = [float(x) for x in bbox_str.split(',')]
    bounds = dict(zip(['west','south','east','north'], bbox))

    query = {
        "from" : 0, 
        "size" : PAGE_SIZE,
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

    return jsonify({
        'type': 'FeatureCollection',
        'features': features
    })


if __name__ == '__main__':
    app.run(debug=True)
