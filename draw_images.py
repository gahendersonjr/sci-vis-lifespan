import pickle
import numpy as np
import random
import csv

country_points = pickle.load(open("country_points.p", "rb"))

lex_map = {}

with open('lex.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    years = next(reader)[4:]
    for row in reader:
        country_code = row[2].upper()
        if country_code in country_points.keys():
            lex_map[country_code] = {}
            lex = row[4:]
            for i in range(0, len(lex)):
                if lex[i] != "":
                    lex_map[country_code][years[i]] = float(lex[i])




for year in years:
    print(year, flush=True)
    image = np.zeros((94, 450, 900), dtype=np.int8)
    for country in country_points.keys():
        if country in lex_map.keys() and year in lex_map[country].keys():
            lifespan = lex_map[country][year]
            for point in country_points[country]:
                x = point[0]
                y = point[1]
                if x % 4 == 0 and y % 4 == 0:
                    for z in range(0,int(lifespan)):
                        image[z][int(y/4)-1][int(x/4)-1] = z

    f = open("lex" + year + ".raw", "wb")
    f.write(bytes(image))
    f.close()
