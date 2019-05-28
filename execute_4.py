# WPS Execute Operation
# for assignment "get street lengths within buffer of the center of EVERY neighborhood"

import requests, json, os

wpsServerUrl = "http://130.89.221.193:85/geoserver/ows?"

# server refuses to give acceses to a python client request without a user header, so I just read neighborhood json from file
jsonfile = open(os.path.dirname(os.path.abspath(__file__)) +"\\neighborhood.json")  
neighborhood = json.load(jsonfile)
name_list = []
for feature in neighborhood['features']:
    if (feature['properties']['gm_name'] == 'Enschede'):  # for simplicity reasons, otherwise it takes FOREVER to process every neighborhood
        name = feature['properties']['bu_name']
        name = name.replace(' ', '%20')  # to make proper urls, remove spaces in the names
        if "'" not in name:  # currently cannot deal with the ' in urls, (e.g., 't Kip), so discard them
            name_list.append(name) 

result = []

for burname in name_list[:3]:  # just take 3 for example, otherwise it takes way too long. 
    # this pay load is from XML file: assignment_2.XML, see XML file for better readability. 
    payload = '''
    <wps:Execute version="1.0.0" service="WPS" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.opengis.net/wps/1.0.0" xmlns:wfs="http://www.opengis.net/wfs" xmlns:wps="http://www.opengis.net/wps/1.0.0" xmlns:ows="http://www.opengis.net/ows/1.1" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:wcs="http://www.opengis.net/wcs/1.1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="http://www.opengis.net/wps/1.0.0 http://schemas.opengis.net/wps/1.0.0/wpsAll.xsd">
    <!-- Execute Length -->
    <ows:Identifier>gs:Length</ows:Identifier>
    <wps:DataInputs>
        <wps:Input>
        <!-- Input feature for Length, from Intersection -->
            <ows:Identifier>feature</ows:Identifier>
            <wps:Reference mimeType="text/xml" xlink:href="http://geoserver/wps" method="POST">
                <wps:Body>
                    <!-- Execute Intersection -->
                    <wps:Execute version="1.0.0" service="WPS">
                    <ows:Identifier>gs:IntersectionFeatureCollection</ows:Identifier>
                    <wps:DataInputs>
                        <wps:Input>
                        <!-- input buffers for Intersection-->
                            <ows:Identifier>first feature collection</ows:Identifier>
                            <wps:Reference mimeType="text/xml" xlink:href="http://geoserver/wps" method="POST">
                                <wps:Body>
                                    <!-- Execute Point Buffer -->
                                    <wps:Execute version="1.0.0" service="WPS">
                                    <ows:Identifier>gs:BufferFeatureCollection</ows:Identifier>
                                    <wps:DataInputs>
                                        <wps:Input>
                                        <!-- Input features to buffer, from Centroid -->
                                            <ows:Identifier>features</ows:Identifier>
                                            <wps:Reference mimeType="text/xml" xlink:href="http://geoserver/wps" method="POST">
                                                <wps:Body>
                                                    <!-- Execute Centroid -->
                                                    <wps:Execute version="1.0.0" service="WPS">
                                                        <ows:Identifier>gs:Centroid</ows:Identifier>
                                                        <wps:DataInputs>
                                                            <wps:Input>
                                                                <ows:Identifier>features</ows:Identifier>
                                                                <!-- neighborhood -->
                                                                    <wps:Reference mimeType="application/json" xlink:href="https://gisedu.itc.utwente.nl/cgi-bin/mapserv.exe?map=d:/iishome/exercise/data/afrialiance/layers.map&amp;version=2.0.0&amp;service=WFS&amp;request=GetFeature&amp;typeName=neighbourhood&amp;outputFormat=geojson&amp;srsname=EPSG:28992&amp;buname=%s" method="GET"/>  
                                                            </wps:Input>
                                                        </wps:DataInputs>
                                                        <!-- Response Centroid -->
                                                        <wps:ResponseForm>
                                                            <wps:RawDataOutput mimeType="application/json">
                                                            <ows:Identifier>result</ows:Identifier>
                                                            </wps:RawDataOutput>
                                                            </wps:ResponseForm>
                                                        </wps:Execute>
                                                </wps:Body>
                                            </wps:Reference>
                                        </wps:Input>
                                        <wps:Input>
                                            <ows:Identifier>distance</ows:Identifier>
                                            <wps:Data>
                                                <wps:LiteralData>1000</wps:LiteralData>
                                            </wps:Data>
                                        </wps:Input>
                                    </wps:DataInputs>
                                    <!-- Response Buffer -->
                                    <wps:ResponseForm>
                                        <wps:RawDataOutput mimeType="application/json">
                                        <ows:Identifier>result</ows:Identifier>
                                        </wps:RawDataOutput>
                                    </wps:ResponseForm>
                                    </wps:Execute>
                                </wps:Body>
                            </wps:Reference>
                        </wps:Input>
                        <!-- input streets for Intersection-->
                        <wps:Input>
                            <ows:Identifier>second feature collection</ows:Identifier>
                            <wps:Reference mimeType="application/json" xlink:href="https://gisedu.itc.utwente.nl/cgi-bin/mapserv.exe?map=d:/iishome/exercise/data/afrialiance/layers.map&amp;version=2.0.0&amp;service=WFS&amp;request=GetFeature&amp;typeName=streets&amp;outputFormat=geojson&amp;srsname=EPSG:28992" method="GET"/>
                        </wps:Input>
                    </wps:DataInputs>
                    <!-- Response Intersection -->
                    <wps:ResponseForm>
                        <wps:RawDataOutput mimeType="application/json">
                        <ows:Identifier>result</ows:Identifier>
                        </wps:RawDataOutput>
                    </wps:ResponseForm>
                    </wps:Execute>
                </wps:Body>
            </wps:Reference>
        </wps:Input>
    </wps:DataInputs>
    <!-- Main Response -->
    <wps:ResponseForm>
        <wps:RawDataOutput mimeType="application/json">
        <ows:Identifier>result</ows:Identifier>
        </wps:RawDataOutput>
    </wps:ResponseForm>
    </wps:Execute>
    '''%(burname)

    length = requests.post(wpsServerUrl, data=payload).text
    result.append({"neighbourhood name": burname.replace('%20', " "), "length": float(length)})

# print("Content-type: application/json")
print("Content-type: text/plain")
print()
print(result)