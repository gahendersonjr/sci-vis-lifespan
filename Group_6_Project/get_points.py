import json
from shapely.geometry import shape, Point
import numpy as np
import math
import pickle
import os
import time

## load geojson
with open('countries.geojson') as f:
    js = json.load(f)

## load pickle file if exists
if os.path.isfile("country_points.p"):
    country_points = pickle.load(open("country_points.p", "rb"))
else:
    country_points = {"ATA": []} #initialize with antarctica since it will take a lot of time for no data

if os.path.isfile("country_points_timer.p"):
    timer = pickle.load(open("country_points_timer.p", "rb"))
    print("continuing timer from " + str(timer))
else:
    timer = 0

for country in js['features']:
    country_code = country['properties']['ISO_A3']
    if  country_code not in country_points.keys():
        start = time.time()
        print("getting points for " + country_code, flush=True)
        points = []
        polygon = shape(country['geometry'])
        bounds = polygon.bounds
        min_x_index = math.floor(bounds[0]*10)
        min_y_index = math.floor(bounds[1]*10)
        max_x_index = math.ceil(bounds[2]*10)
        max_y_index = math.ceil(bounds[3]*10)
        for x in range(min_x_index, max_x_index):
            if x % 10 == 0:
                print(str(x/10) + "/" + str(max_x_index/10), flush=True)
            for y in range(min_y_index, max_y_index):
                if polygon.contains(Point(x/10, y/10)):
                    points.append((x+1800, y+900))
        country_points[country_code] = points
        pickle.dump(country_points, open( "country_points.p", "wb" ))
        timer += (time.time()-start)
        pickle.dump(timer, open( "country_points_timer.p", "wb" ))
    else:
        print("skipping " + country_code, flush=True)
