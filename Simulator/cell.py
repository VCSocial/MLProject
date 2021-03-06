import math
from .Depencencies.graphics import Rectangle, color_rgb
from .Depencencies.graphics import Point


class Cell:
    __COMPASS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

    def __init__(self, attr, pt1, pt2,
                 moves=[0.71428, 0.71428, 0.71428, 0.71428, 0.71428, 0.71428, 0.71428, 0.71428],
                 block=False, windy=False, dir=0, intensity=0.0):
        self.attribs = attr
        self.blocked = block

        # Generate a new tile
        self.tile = Rectangle(pt1, pt2)
        #self.tile.setOutline('white')
        # N NE E SE S SW W NW
        if self.blocked:
            self.move_cost = [math.inf, math.inf, math.inf, math.inf,
                               math.inf, math.inf, math.inf, math.inf]
            self.marker = 'X'
            self.tile.setOutline('brown')
            self.tile.setFill('brown')
        else:
            self.move_cost = moves
            self.marker = 'O'
            # color_rgb('85','170','255')
            self.tile.setOutline('blue')
            self.tile.setFill('blue')

            # Reduce cost by intensity
            if windy:
                self.move_cost[dir] -= intensity


        self.visited = False
        self.here = False
        self.explored = 0 # scale from 0% to 100%


    def print_attribs(self):
        print(self.attribs)

    def get_attribs(self):
        return self.attribs if (not self.blocked) else None

    def visit(self):
        self.visited = True
        self.here = True
        self.tile.setFill('black')
        self.marker = '@'

    def leave(self):
        self.here = False
        self.tile.setFill('yellow')
        self.marker = '$'

    def explore(self, percentage):
        if self.marker == 'X':
            self.explored = 0
        else:
            self.explored = percentage
        self.marker = '~' + str(self.explored)if not self.here else '@'

        if not self.here and not self.visited :
            self.tile.setFill('orange')

        if percentage - self.explored > 0:
            return percentage - self.explored

        return 0


    def get_symbol(self):
        return self.marker

    def cell_stats(self):
        return self.explored

    def get_tile(self):
        return self.tile

    def get_costs(self):
        print(self.move_cost)
        return self.move_cost

    def is_visited(self):
        return self.visited

