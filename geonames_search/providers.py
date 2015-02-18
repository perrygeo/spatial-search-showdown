import json

def postgis(bounds, conn, sql):
    result = conn.execute(sql, **bounds)
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


def elasticsearch(bounds, session, URL):
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
