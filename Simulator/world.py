import pandas as pd
import numpy as np
import datetime as dt
import random
#import matplotlib.pyplot as plt
#import matplotlib
import PIL
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#from matplotlib.figure import Figure

# User generated classes
from .osmparser import OSMParser
from .cell import Cell
from .vehicle import Vehicle
from .train import Train
from .LearningAlgorithms.policy import Policy


# Hard dep on this package for graphics
from .Depencencies.graphics import *

class World:
    """ Generate the grid world for ML"""
    __LOGGING_LEVEL = 0

    def __init__(self, file_path, lvl=1):
        World.__LOGGING_LEVEL = lvl
        try:
            o = OSMParser(file_path)
            grid, attrs = o.retrieve_mapping()
        except FileNotFoundError as err:
            print(err)
        else:
            title = "GridWorld: " + file_path

            trainer = Train(o)
            x, y = trainer.get_start()
            self.actions = trainer.retrieve_actions()
            
            
            self.actions = [1, 7, 1, 7, 7, 7, 1, 1, 2, 2, 1, 1, 1, 1, 3, 3, 1, 1, 3, 1, 3, 3, 4, 5, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 5, 5, 3, 3, 1, 3, 3, 2, 3, 1, 7, 0, 1, 1, 1, 1, 1, 0, 2, 2, 3, 3, 1, 1, 3, 1, 3, 2, 3, 4, 3, 2, 3, 3, 1, 1, 1, 3, 3, 2, 3, 1, 1, 0, 1, 1, 7, 7, 7, 0, 1, 7, 1, 7, 7, 7, 6, 7, 6, 5, 5, 5, 5, 5, 7, 7, 7, 7, 7, 1, 1, 7, 7, 7, 5, 5, 6, 7, 5, 6, 5, 6, 5, 7, 5, 5, 4, 5, 7, 4, 7, 4, 0, 6, 7, 6, 7, 6, 7, 6, 7, 6, 7, 6, 6]
            print(len(self.actions))
            self.init_gui(grid, attrs, title)
            self.init_simulation(x, y)



    def init_gui(self, grid, attrs, title):
        lim_y = len(grid)
        lim_x = len(grid[0])

        print("Board dimensions:", lim_x, ",", lim_y)

        # Build the window
        cell_sz = 8
        self.win = GraphWin(title, lim_x * cell_sz,
                            lim_y * cell_sz + cell_sz * 2)
        self.win.setBackground('black')

        dummy_atr = 'I\'m a gnome, and you got gnomed!'

        print("Generating graphical representation")
        gph_x = 0
        gph_y = 0

        # Total possible explorable tiles
        self.exploration_potential = 0
        self.explored_so_far = 0


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

        self.txt = Text(Point(lim_x * cell_sz / 2, lim_y * cell_sz + 1 * cell_sz), "")
        self.txt.setTextColor('white')
        self.txt.setFace("courier")
        self.txt.setText("To begin the simulation press W")
        self.txt.draw(self.win)

        # lwr_graph = "lwr_graph.png"
        # lwr_fig = matplotlib.pyplot.figure()
        # lwr_fig.suptitle('Exploration Ratio')
        # sub = lwr_fig.add_subplot(111)
        # sub.plot(100, (100.0 / self.exploration_potential) *
        #               self.explored_so_far)
        # lwr_fig.savefig(lwr_graph)
        #
        # im_offset_x = (lim_x * cell_sz) + (lim_x * cell_sz / 2)
        # im_offset_upr_y = (lim_y * cell_sz / 2)
        #
        # exp_img = Image(Point(im_offset_x, im_offset_upr_y), lwr_graph,
        #                 width=int(lim_x * cell_sz),
        #                 height=int((lim_y * cell_sz) / 2))
        # exp_img.draw(self.win)
        #
        # matplotlib.pyplot.close()

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
                    if j < 0 or i < 0:
                        continue

                    e = 0
                    if (self.real_grid[i][j]).cell_stats() != 100:
                        # If it is horizontal/ vertical
                        if i == cur_x or j == cur_y:
                            e = (self.real_grid[i][j]).explore(80)
                            e = 80

                        # Otherwise the choice is diagonal
                        elif not ((self.real_grid[i][j]).cell_stats() > 40):
                            e = (self.real_grid[i][j]).explore(40)
                            e = 40
                    e = 0 
                    self.explored_so_far += e
                    print(self.explored_so_far, e)
                    # TODO: Is this really necessary?
                    exp_rate.append((self.real_grid[i][j]).cell_stats())

                    # Do not record the current location
                    if cur_x == i and cur_y == j:
                        continue
                    coords.append([i, j])
                except IndexError:
                    continue

        if World.__LOGGING_LEVEL == 1:
            print("Moves found:", coords)

        return exp_rate, coords


    def interaction(self):


        #while self.win.checkKey() != 'w':
        #    if self.win.checkKey() == 'q':
        #        self.judgement_day()
        #    continue
        self.win.update()

    def init_simulation(self, init_x=0, init_y=0):
        if World.__LOGGING_LEVEL == 1:
            print("*** Initializing simulation!")
            print("*** SYMBOL:",self.real_grid[init_x][init_y].get_symbol())

        while self.real_grid[init_x][init_y].get_symbol() == 'X':
            init_y = random.randint(0, len(self.real_grid) - 1)
            init_x = random.randint(0, len(self.real_grid[0]) - 1)
            if World.__LOGGING_LEVEL == 1:
                 print("*** Invalid start finding new start")
                 print("*** Coordinates found:", init_x, init_y)
                 print("*** Range x:", len(self.real_grid[0]) -1, "Range y:",
                       len(self.real_grid) -1)

        self.uav = Vehicle(init_x, init_y)
        (self.real_grid[init_x][init_y]).visit()
        (self.real_grid[init_x][init_y]).explore(100)
        #self.explored_so_far += (self.real_grid[init_x][init_y]).cell_stats()
        self.explored_so_far += 100
        self.inspect_radius(init_x, init_y)

        bat = "BAT:" + "{:.2f}".format(self.uav.get_bat()) + "/100 "
        per = "{:.4f}".format(100.0 / self.exploration_potential * self.explored_so_far)


        msg = "INIT \t(" + str(per) + "% explored" + ")\t " + bat + "Lat: " \
              + str(init_x) + " Lon: " + str(init_y)
        self.txt.setText(msg)
        self.interaction()


    def traverse(self, direction):
        #TODO Dirty hack here, improve implementation
        i, j = self.uav.get_coords()
        costs = (self.real_grid[i][j]).get_costs()
        x, y, old_x, old_y = self.uav.move(direction, costs,
                                           self.real_grid)

        if World.__LOGGING_LEVEL == 1:
            print("MOVING from", old_x, old_y)
            print("MOVING to", x, y)

        try:
            (self.real_grid[old_x][old_y]).leave()
            (self.real_grid[x][y]).explore(100)

            if not (self.real_grid[x][y]).is_visited():
                print("visit so far ", self.explored_so_far)
                self.explored_so_far += (self.real_grid[x][y]).cell_stats()
            
            (self.real_grid[x][y]).visit()
            self.inspect_radius(x, y)
        except:
            print("Trying to exit World")

        bat = "BAT:" + "{:.2f}".format(self.uav.get_bat()) + "/100 "
        per = "{:.4f}".format(100.0 / self.exploration_potential * self.explored_so_far)
    
        print("POTENTIAL", self.exploration_potential)
        print("SO FAR", self.explored_so_far)

        if x == old_x and y == old_y:
            msg = "WAIT \t(" + str(per) + "% explored" + ")\t " + bat + "Lat: " \
                  + str(x) + " Lon: " + str(y)
        else:
            msg = "MOVE \t(" + str(per) + "% explored" + ")\t " + bat + "Lat: " \
                  + str(x) + " Lon: " + str(y)
        self.txt.setText(msg)
        self.interaction()

        if World.__LOGGING_LEVEL == 2:
            fname = str(dt.datetime.now()) + "_move.csv"
            self.pretty_print(os.path.join("./Output/", fname))

    def navigate_with_policy(self):
        print(self.actions)

        # Run through the optimal path
        for i in range(len(self.actions)):

            # Exit if we run out of battery
            if self.uav.bat <= 0:
                print(">>>> Ran out of battery!")
                break

            try:
                x, y = self.uav.get_coords()
                self.inspect_radius(x, y)
                self.traverse(self.actions[i])
                print(">>>> Moving according to optimal action")
                print(">>>> Current action:", self.actions[i])

            except:
                if World.__LOGGING_LEVEL >= 1:
                    print(">>>> Exception executing optimal path!")

        for i in range(10):
            print("Consumed all available actions! EXITING NOW!")


    def navigate_with_policy_legacy(self):
        p = Policy()

        while self.uav.bat - 0.71428 > 0:
            try:
                x, y = self.uav.get_coords()
                opts, coords = self.inspect_radius(x, y)
                pos = [x, y]


                print("In policy")

                # Get the cheapest move based on our current location
                d = p.random_move(pos, opts, coords)
                print("Still policy")
                self.traverse(d)
                print("Also still")
            except:
                print("POLICY FAILURE")
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
        while self.win.checkKey() != 'q':
            continue
        self.win.close()

