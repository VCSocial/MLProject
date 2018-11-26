import xml.etree.ElementTree as et
import pandas as pd
import numpy as np

class OSMParser:

    def __init__(self):
        tree = et.parse('map_2.osm')

        bounds = tree.find('bounds')
        minlat = bounds.get('minlat')
        minlon = bounds.get('minlon')
        maxlat = bounds.get('maxlat')
        maxlon = bounds.get('maxlon')

        print(minlat, minlon, maxlat, maxlon)


        id = []
        lat = []
        lon = []

        root = tree.getroot()
        for node in root.iter('node'):
            # if not (node.get('lat') <= maxlat and node.get('lat') >= minlat):
            #     continue
            # if not (node.get('lon') <= maxlon and node.get('lon') >= minlon):
            #     continue
            id.append(node.get('id'))
            lat.append(node.get('lat'))
            lon.append(node.get('lon'))

        water_found = False
        water_nds = []
        for way in root.iter('way'):
            for tag in way.iter('tag'):
                if (tag.get('k') == 'natural' and tag.get('v') == 'water'): #or tag.get('k') == 'waterway':
                    water_found = True
                    break
            if water_found:
                for nd in way.iter('nd'):
                    water_nds.append(nd.get('ref'))
                water_found = False


        df_wat = pd.DataFrame(
            np.column_stack([water_nds]),
            columns=['refs']
        )

        df = pd.DataFrame(
            np.column_stack([id, lat, lon]),
            columns=['ids','lats','lons']
        )

        print(df_wat)
        df.to_csv('outfile.csv')
        self.make_grid(df, df_wat)

    def make_grid(self, df, df2):
        limit = int(np.sqrt(df.shape[0]) + 1) #43
        print(limit)
        self.real_grid = []
        for row in range(limit):
            self.real_grid += [['X'] * limit]

        # Build the window

        len_X = len(self.real_grid)
        len_Y = len(self.real_grid[0])
        idx = 0

        grphx_x = 0
        grphx_y = 0
        end_loop = False
        for y in range(len_Y):
            for x in range(len_X):
                try:
                    row = df.iloc[idx, :]
                    curr_attr = [row['ids'], row['lats'], row['lons']]
                    if row['ids'] in df2['refs'].values:
                        self.real_grid[x][y] = 'O'
                    idx += 1
                except IndexError:
                    print("DataFrame Exhausted. Terminating loading!")
                    end_loop = True
                    break
            if end_loop:
                break

            out_df = pd.DataFrame(np.array(self.real_grid))
            out_df.to_csv("relative_grid.csv")



o = OSMParser()
