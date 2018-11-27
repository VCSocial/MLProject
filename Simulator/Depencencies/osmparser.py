import xml.etree.ElementTree as et
import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from pyproj import Proj, transform
import math

class OSMParser:

    def __init__(self):
        tree = et.parse('map.xml')

        id  = []
        lat = []
        lon = []
        root = tree.getroot()
        water_id = []
        fd_water = False
        for way in root.iter('way'):
            for tag in way.iter('tag'):
                if (tag.get('k') == "natural" and tag.get('v') == "water") or tag.get('k') == "waterway":
                    fd_water = True

            if fd_water:
                for nd in way.iter('nd'):
                    water_id.append(nd.get('ref'))

            fd_water = False



        for node in root.iter('node'):
            # if (float(node.get('lat')) <= maxlat and float(node.get('lat')) >= minlat) and \
            #        (float(node.get('lon')) <= maxlon and float(node.get('lon')) >= minlon):
            if node.get('id') in water_id:
                id.append(node.get('id'))
                lat.append(float(node.get('lat')))
                lon.append(float(node.get('lon')))




        # id_water = []
        # for way in root.iter('way'):
        #
        #     for nd way.iter('nd'):
        #plt.scatter(lat,lon)
        #plt.show()


        minlat = min(lat)
        minlon = min(lon)
        maxlat = max(lat)
        maxlon = max(lon)

        print(minlat, minlon, maxlat, maxlon)
        lower = maxlat - minlat
        upper = maxlon - minlon
        j = int(math.sqrt(len(water_id)) + 1)

        div_low = lower / j
        div_upp = upper / j

        clat = []
        clon = []

        for i in range(0, j + 1):
            clat.append(minlat + (i * div_low))

        for i in range(0, j + 1):
            clon.append(minlon + (i * div_upp))


        print(clat)
        print("*******************")
        print(clon)

        grid_lat = [-1] * j
        grid_lon = [-1] * j

        grid = []
        for row in range(j):
            grid += [['&'] * j]


        overwrites = 0
        for k in range(len(lat)):
            print(lat[k], lon[k])

            for i in range(0, j - 1):
                m = (lat[k] > clat[i])
                n = (lat[k] < clat[i + 1])
                if m and n:
                    if lat[k]-clat[i] > lat[i+1]-lat[k]:
                        grid_lat[i+1] = lat[k]
                    else:
                        grid_lat[i] = lat[k]
            print(grid_lat)

            for i in range(0, j - 1):
                m = (lon[k] > clon[i])
                n = (lon[k] < clon[i + 1])
                #print(lon[k], clon[i], clon[i+1])
                if m and n:
                    #print("*****************")
                    if lon[k]-clon[i] > lon[i+1]-lon[k]:
                        grid_lon[i+1] = lon[k]
                    else:
                        grid_lon[i] = lon[k]

            print(grid_lon)
            try:
                if grid[grid_lat.index(lat[k])][grid_lon.index(lon[k])] == 'X':
                    overwrites += 1
                    #grid[grid_lat.index(lat[k]) + 1][grid_lon.index(lon[k]) + 1]

                grid[grid_lat.index(lat[k])][grid_lon.index(lon[k])] = 'X'
            except:
                print("NOT IN LIST")

        print(overwrites, "overwritten cells")

        # Horizontal Pass
        for y in range(j):
            try:
                init = grid[y].index('X')
                term = len(grid[y]) - grid[y][::-1].index('X') - 1
                print("First occurrence at:", init, "last occurrence at:", term)
                for x in range (init + 1, term):
                    grid[y][x] = 'X'
            except:
                print("NOT IN LIST")

        # Vertical Pass
        activ_pass = False
        for x in range(j):
            for y in range(j):
                try:
                    if grid[y][x] == '&' and grid[y + 1][x] == 'X':
                        activ_pass = True
                    if grid[y][x] == 'X' and grid[y + 1][x] == '&':
                        activ_pass = False
                    if activ_pass:
                        grid[y][x] = 'X'
                except:
                    print("Out of Range")


        df = pd.DataFrame(np.array(grid))
        df.to_csv('new_test.csv')

o = OSMParser()
