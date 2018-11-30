import pandas as pd
import numpy as np
import datetime as dt
import random

# User generated classes
from .osmparser import OSMParser
from .cell import Cell
from .vehicle import Vehicle
from .LearningAlgorithms.policy import Policy

# Hard dep on this package for graphics
from .Depencencies.graphics import *

class GenWorld:
    """ Generate the grid world for ML"""
    __LOGGING_LEVEL = 0

    def __init__(self, file_path, lvl=1):
        GenWorld.__LOGGING_LEVEL = lvl
        try:
            o = OSMParser(file_path)
            grid, attrs = o.retrieve_mapping()
        except FileNotFoundError as err:
            print(err)
        else:
            title = "GridWorld: " + file_path

            #self.make_grid(title)
            self.init_gui(grid, attrs, title)
            self.init_simulation()


    def init_gui(self, grid, attrs, title):
        lim_y = len(grid)
        lim_x = len(grid[0])

        print("Board dimensions:", lim_x, ",", lim_y)

        # Build the window
        cell_sz = 8
        self.win = GraphWin(title, lim_x * cell_sz + lim_x * cell_sz,
                            lim_y * cell_sz + cell_sz * 2)
        self.win.setBackground('black')

        dummy_atr = 'I\'m a gnome, and you got gnomed!'

        print("Generating graphical representation")
        gph_x = 0
        gph_y = 0

        # Total possible explorable tiles
        self.exploration_potential = 0
        for y in range(lim_y):
            for x in range(lim_x):
                upr = Point(gph_x, gph_y)
                lwr = Point(gph_x + cell_sz, gph_y + cell_sz)
                grid[y][x] = Cell(dummy_atr, upr, lwr,
                                  block=False if grid[y][x] == 'O' else True)

                if (grid[y][x]).get_symbol() == 'O':
                    self.exploration_potential += 100

                ((grid[y][x]).get_tile()).draw(self.win)
                gph_x += cell_sz

            gph_x = 0
            gph_y += cell_sz

        print("Finished generation")
        print("Total exploration potential:", self.exploration_potential)
        self.real_grid = grid

        border_width = 2
        gph_x = lim_x * cell_sz
        gph_y = 0
        for x in range(border_width):
            for y in range(lim_y * cell_sz + cell_sz * 2):
                p1 = Point(gph_x, gph_y)
                p2 = Point(gph_x + cell_sz, gph_y + cell_sz)
                border = Rectangle(p1, p2)
                border.setFill(color_rgb(49, 54, 59))
                border.setOutline(color_rgb(49, 54, 59))
                border.draw(self.win)
                gph_y += cell_sz

            gph_x += cell_sz
            gph_y = 0

        self.txt = Text(Point(lim_x * cell_sz / 2, lim_y * cell_sz + 1 * cell_sz), "")
        self.txt.setTextColor('white')
        self.txt.setFace("courier")
        self.txt.setText("To begin the simulation press W")
        self.txt.draw(self.win)

        self.interaction()


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

                    # If it is horizontal/ vertical
                    if i == cur_x or j == cur_y:
                        (self.real_grid[i][j]).explore(80)

                    # Otherwise the choice is diagonal
                    elif not ((self.real_grid[i][j]).cell_stats() > 40):
                        (self.real_grid[i][j]).explore(40)

                    exp_rate.append((self.real_grid[i][j]).cell_stats())

                    # Do not record the current location
                    if cur_x == i and cur_y == j :
                        continue

                    coords.append([i, j])
                except IndexError:
                    continue

        if GenWorld.__LOGGING_LEVEL == 1:
            print("Moves found:", coords)

        return exp_rate, coords

    def interaction(self):

        while self.win.checkKey() != 'w':
            if self.win.checkKey() == 'q':
                self.judgement_day()
            continue
        self.win.update()

    def init_simulation(self, init_x=0, init_y=0):
        if GenWorld.__LOGGING_LEVEL == 1:
            print("Initializing simulation!")
            print("SYMBOL:",self.real_grid[init_x][init_y].get_symbol())

        while self.real_grid[init_x][init_y].get_symbol() == 'X':
            init_y = random.randint(0, len(self.real_grid) - 1)
            init_x = random.randint(0, len(self.real_grid[0]) - 1)
            if GenWorld.__LOGGING_LEVEL == 1:
                 print("Invalid start finding new start")
                 print("Coordinates found:", init_x, init_y)
                 print("Range x:", len(self.real_grid[0]) -1, "Range y:", len(self.real_grid) -1)

        self.uav = Vehicle(init_x, init_y)
        (self.real_grid[init_x][init_y]).visit()
        (self.real_grid[init_x][init_y]).explore(100)
        self.inspect_radius(init_x, init_y)

        msg = "INIT \t\t\t\t\t\t Lat: " + str(init_x) + \
              " Lon: " + str(init_y)
        self.txt.setText(msg)
        self.interaction()


    def traverse(self, direction):
        #TODO Dirty hack here, improve implementation
        i, j = self.uav.get_coords()
        costs = (self.real_grid[i][j]).get_costs()
        x, y, old_x, old_y = self.uav.move(direction, costs,
                                           self.real_grid)

        if GenWorld.__LOGGING_LEVEL == 1:
            print("MOVING from", old_x, old_y)
            print("MOVING to", x, y)

        try:
            (self.real_grid[old_x][old_y]).leave()
            (self.real_grid[x][y]).visit()
            self.inspect_radius(x, y)
        except:
            print("Trying to exit World")

        if x == old_x and y == old_y:
            msg = "WAIT \t\t\t\t\t\t Lat: " + str(x) + \
                " Lon: " + str(y)
        else:
            msg = "MOVE \t\t\t\t\t\t Lat: " + str(x) + \
                  " Lon: " + str(y)
        self.txt.setText(msg)
        self.interaction()

        if GenWorld.__LOGGING_LEVEL == 2:
            fname = str(dt.datetime.now()) + "_move.csv"
            self.pretty_print(os.path.join("./Output/", fname))


    def navigate_with_policy(self):
        p = Policy()

        while self.uav.bat > 0:
            try:
                x, y = self.uav.get_coords()
                opts, coords = self.inspect_radius(x, y)
                pos = [x, y]

                # Get the cheapest move based on our current location
                d = p.random_move(pos, opts, coords)
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

