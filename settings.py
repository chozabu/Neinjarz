"""settings.py: loads settings json file."""

__author__ = "Alex 'Chozabu' P-B"
__copyright__ = "Copyright 2016, Chozabu"

import json


with open('default_settings.json') as json_data:
    jdata = json.load(json_data)
    print(jdata)

try:
    with open('settings.json') as json_data:
        jdata = json.load(json_data)
        print("using local settings")
        print(jdata)
except:
    print("using default settings")
