import pandas as pd
import numpy as np
import datetime as dt
import os

# User generated classes
from .cell import Cell
from .vehicle import Vehicle
from .LearningAlgorithms.policy import Policy

# Hard dep on this package for graphics
from .Depencencies.graphics import *

# import pygame as pg

class GenWorld:
    """ Generate the grid world for ML"""
    __LOGGING_LEVEL = 0

    def __init__(self, file_path, lvl=2):
        GenWorld.__LOGGING_LEVEL = lvl
        try:
            pd.set_option("display.precision", 32)
            self.grid_df = pd.read_csv(file_path, sep=";",  na_values=['(NA)']).fillna(0)
        except FileNotFoundError as err:
            print(err)
        else:
            title = "GridWorld: " + file_path
            self.make_grid(title)
            self.init_simulation()
            self.pretty_print()


    def print_df(self, head=True, sz=5):
        print(self.grid_df.head(sz) if head else self.grid_df)


    def make_grid(self, title):
        limit = int(np.sqrt(self.grid_df.shape[0]) + 1) #43
        if GenWorld.__LOGGING_LEVEL == 1:
            print(limit)
        self.real_grid = []
        for row in range(limit):
            self.real_grid += [['X'] * limit]

        # Build the window
        cell_sz = 16
        self.win = GraphWin(title, limit * cell_sz + limit * cell_sz, limit * cell_sz)
        self.win.setBackground('black')

        len_X = len(self.real_grid)
        len_Y = len(self.real_grid[0])
        idx = 0

        grphx_x = 0
        grphx_y = 0
        end_loop = False
        for y in range(len_Y):
            for x in range(len_X):
                try:
                    row = self.grid_df.iloc[idx, :]
                    curr_attr = [row['Latitude'], row['Longitude'], row['Time']]
                    self.real_grid[x][y] = Cell(curr_attr, Point(grphx_x,grphx_y),
                                                Point(grphx_x + cell_sz,
                                                      grphx_y + cell_sz))

                    idx += 1
                except IndexError:

                    self.real_grid[x][y] = Cell(['LAND'], Point(grphx_x, grphx_y),
                                                Point(grphx_x + cell_sz,
                                                      grphx_y + cell_sz),
                                                block=True)

                    #print("DataFrame Exhausted. Terminating loading!")
                    # end_loop = True
                    # break

                ((self.real_grid[x][y]).get_tile()).draw(self.win)
                grphx_x += cell_sz
            grphx_x = 0
            grphx_y += cell_sz
            # if end_loop:
            #     break

        while self.win.checkKey() != 'w':
            continue
        self.win.redraw()

        if GenWorld.__LOGGING_LEVEL == 1:
            print(np.array(self.real_grid))
        if GenWorld.__LOGGING_LEVEL == 2:
            df = pd.DataFrame(np.array(self.real_grid))
            df.to_csv("relative_grid.csv")



    def inspect_radius(self, cur_x, cur_y):
        init_x = cur_x - self.uav.get_radius()
        init_y = cur_y - self.uav.get_radius()
        term_x = cur_x + self.uav.get_radius() + 1
        term_y = cur_y + self.uav.get_radius() + 1
        coords = []
        exp_rate = []

        for j in range(init_y, term_y):
            for i in range(init_x, term_x):
                try:
                    # Avoid out of bounds or overwriting visited
                    if j < 0 or i < 0 \
                            or (self.real_grid[i][j]).cell_stats() == 100:
                        continue
                    if i == cur_x or j == cur_y:
                        # If it is horizontal/ vertical
                        (self.real_grid[i][j]).explore(80)
                    elif not ((self.real_grid[i][j]).cell_stats() > 40):
                        # Otherwise it is diagonal
                        (self.real_grid[i][j]).explore(40)

                    exp_rate.append((self.real_grid[i][j]).cell_stats())
                    coords.append([i, j])
                except IndexError:
                    #print("Out of Bounds.")
                    continue

        return exp_rate, coords


    def init_simulation(self, init_x=0, init_y=0):
        self.uav = Vehicle()
        (self.real_grid[init_x][init_y]).visit()
        (self.real_grid[init_x][init_y]).explore(100)
        self.inspect_radius(init_x, init_y)

        while self.win.checkKey() != 'w':
            continue
        self.win.redraw()


    def traverse(self, direction):
        #TODO Dirty hack here, improve implementation
        i, j = self.uav.get_coords()
        costs = (self.real_grid[i][j]).get_costs()
        x, y, old_x, old_y = self.uav.move(direction, costs)

        print("MOVING from", old_x, old_y)
        print("MOVING to", x, y)
        try:
            (self.real_grid[old_x][old_y]).leave()
            (self.real_grid[x][y]).visit()
            self.inspect_radius(x, y)
        except:
            print("Trying to exit World")

        while self.win.checkKey() != 'w':
            continue
        self.win.redraw()

        fname = str(dt.datetime.now()) + "_move.csv"
        self.pretty_print(os.path.join("./Output/", fname))

    def navigate_with_policy(self):
        p = Policy()

        while self.uav.bat > 0:
            try:
                # print("In explore loop")
                x, y = self.uav.get_coords()
                #costs = (self.real_grid[x][y]).get_costs()
                #print("COSTS ARE: ", costs)

                opts, coords = self.inspect_radius(x, y)
                pos = [x, y]

                # Get the cheapest move based on our current location
                d = p.random_move(pos, opts, coords)
                print("Direction is:", d)
                self.traverse(d)
            except:
                continue




    def pretty_print(self, outfile=''):
        limit = len(self.real_grid)
        print_grid = []
        for row in range(limit):
            print_grid += [['X'] * limit]

        for y in range (len(self.real_grid)):
            for x in range(len(self.real_grid[0])):
                try:
                    print_grid[x][y] = (self.real_grid[x][y]).get_symbol()
                except:
                    continue

        df = pd.DataFrame(np.array(print_grid))
        df.to_csv("pretty_grid.csv" if outfile == '' else outfile)

    def judgement_day(self):
        self.win.close()

