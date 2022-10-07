# -*- coding: utf-8 -*-
"""
Created on Tue May  4 20:45:04 2021

@author: user
"""

import requests
import json
def getAir(site):
    url ='https://data.epa.gov.tw/api/v1/aqx_p_432?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&format=json'
    air =json.loads(requests.get(url).text)
    allair = air['records']
    content={}
    for row in allair:
        name = row['SiteName']
        status=row['Status']
        content[name]=status
    return content.get(site,'找不到')

print(getAir('忠明'))