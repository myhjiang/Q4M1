# WPS Execute Operation

import requests, os

payload = open(os.path.dirname(os.path.abspath(__file__)) +"\\convexhull.xml").read()


wpsServerUrl = "https://gisedu.itc.utwente.nl/student/s6039677/gpw/wps.py?"

response = requests.post(wpsServerUrl, data=payload)
print("Content-type: application/json")
print()
print(response.text)