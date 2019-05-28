# ---------------------
# Convex Hull Generation from Feature Collection.  using WPS specification
# ---------------------
from osgeo import ogr
from osgeo import osr
import json

def title():
    return "Convex Hull" # title of the function

def abstract():
    return "A function that returns the convex hull of an input feature collection" # short description of the function

def inputs():
    return [
        ['features', 'Input feature collection','The input feature collection','application/json', True]
    ]

def outputs():
    return [['result', 'convex hull','The convex hull polygon of the input feature collection','application/json']]

def execute(parameters):
    geojson = parameters.get('features')

    if (geojson is not None):
        geojson = geojson['value']
        json_obj = json.loads(geojson)  # needs json object/dict to loop

    # add feature geometries to geometry collection
    geomcol = ogr.Geometry(ogr.wkbGeometryCollection)
    for feature in json_obj['features']:
        geom = feature['geometry']
        geometry = ogr.CreateGeometryFromJson(str(geom)) # string needed here
        geomcol.AddGeometry(geometry)

    # generate convex hull for geometry collection, returns a geometry 
    convexhull = geomcol.ConvexHull()

    print("Content-type: application/json")
    print()
    print(convexhull.ExportToJson())
