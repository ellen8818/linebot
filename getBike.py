# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 21:26:12 2021

@author: user
"""

import requests
import json
def getTPBike():
    
    url = "https://data.ntpc.gov.tw/api/datasets/71CD1490-A2DF-4198-BEF1-318479775E8A/json/?page=0&size=700"
    data = json.loads(requests.get(url).text)
    area = {}
    station = list()
    sbi = list()
    bemp = list()
    lat = list()
    lng = list()
    barea = list()
    for row in data:
        station.append(row['sna'])
        sbi.append(row['sbi'])
        bemp.append(row['bemp'])
        lat.append(float(row['lat']))
        lng.append(float(row['lng']))
        barea.append(row['sarea'])
        
    return station, sbi, bemp
