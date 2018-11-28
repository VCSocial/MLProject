import xml.etree.ElementTree as et
import pandas as pd
import numpy as np
import math

class OSMParser:
    __LOGGING_LVL = 0

    def __init__(self, infile):
        # Open the OSM file for parsing
        tree = et.parse(infile)
        root = tree.getroot()

        # Record nodes which are related to water, waterways, streams, etc...
        water_id = []
        fd_water = False
        for way in root.iter('way'):
            for tag in way.iter('tag'):
                if (tag.get('k') == "natural" and tag.get('v') == "water") or \
                        tag.get('k') == "waterway":
                    fd_water = True

            if fd_water:
                for nd in way.iter('nd'):
                    water_id.append(nd.get('ref'))

            fd_water = False


        # Using node reference load data from relevant nodes
        id  = []
        lat = []
        lon = []

        for node in root.iter('node'):
            if node.get('id') in water_id:
                id.append(node.get('id'))
                lat.append(float(node.get('lat')))
                lon.append(float(node.get('lon')))


        # Setup boundaries and setup grid
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


        grid_lat = [-1] * j
        grid_lon = [-1] * j

        grid = []
        for row in range(j):
            grid += [['X'] * j]


        atr = []
        for k in range(len(lat)):
            if OSMParser.__LOGGING_LVL > 0:
                print(lat[k], lon[k])

            for i in range(0, j - 1):
                m = (lat[k] > clat[i])
                n = (lat[k] < clat[i + 1])
                if m and n:
                    if lat[k]-clat[i] > lat[i+1]-lat[k]:
                        grid_lat[i+1] = lat[k]
                    else:
                        grid_lat[i] = lat[k]
            if OSMParser.__LOGGING_LVL > 0:
                print(grid_lat)

            for i in range(0, j - 1):
                m = (lon[k] > clon[i])
                n = (lon[k] < clon[i + 1])
                if m and n:
                    if lon[k]-clon[i] > lon[i+1]-lon[k]:
                        grid_lon[i+1] = lon[k]
                    else:
                        grid_lon[i] = lon[k]

            if OSMParser.__LOGGING_LVL > 0:
                print(grid_lon)
            try:
                atr.append([id[k], lat[k], lon[k]])
                grid[grid_lat.index(lat[k])][grid_lon.index(lon[k])] = 'O'
            except:
                print("NOT IN LIST")

        # Attempt to fill out distortions caused by projecting
        # sphere surface to 2D grid

        # Horizontal Pass
        for y in range(j):
            try:
                init = grid[y].index('O')
                term = len(grid[y]) - grid[y][::-1].index('O') - 1

                if OSMParser.__LOGGING_LVL > 0:
                    print("First occurrence at:", init, "last occurrence at:", term)
                for x in range(init + 1, term):
                    grid[y][x] = 'O'
            except:
                if OSMParser.__LOGGING_LVL > 0:
                    print("NOT IN LIST")
                continue

        # Vertical Pass
        activ_pass = False
        for x in range(j):
            for y in range(j):
                try:
                    if grid[y][x] == 'X' and grid[y + 1][x] == 'O':
                        activ_pass = True
                    if grid[y][x] == 'O' and grid[y + 1][x] == 'X':
                        activ_pass = False
                    if activ_pass:
                        grid[y][x] = 'O'
                except:
                    if OSMParser.__LOGGING_LVL > 0:
                        print("Out of Range")
                    continue

        if OSMParser.__LOGGING_LVL > 0:
            df = pd.DataFrame(np.array(grid))
            df.to_csv('../Output/new_test.csv')

        self.register_grid(grid, atr)


    def register_grid(self, gd, atr):
        self.grid = gd
        self.attr = atr


    def retrieve_mapping(self):
        return self.grid, self.attr.reverse()
