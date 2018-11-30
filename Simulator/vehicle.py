import math

class Vehicle:

    def __init__(self, init_x=0, init_y=0, bat=100, reg_data_rec=0,
                 local_data_rec=0):
        """ Create a vehicle which navigates out grid world

        :param bat: percentage of battery for the UAV
        :param reg_data_rec: data recorded within the entire region
        :param local_data_rec: data recorded within a local cell
        """
        self.bat = bat
        self.reg_data_rec = reg_data_rec
        self.local_data_rec = local_data_rec

        # Record cells visited
        self.visited = 0
        self.loc = [init_x, init_y]
        self.detection_radius = 1


    def move(self, direction, costs, grid):
        prev = self.loc

        if direction == 0:
            self.loc = [self.loc[0] - 1, self.loc[1]]
        elif direction == 1:
            self.loc = [self.loc[0] - 1, self.loc[1] + 1]
        elif direction == 2:

            self.loc = [self.loc[0], self.loc[1] + 1]
        elif direction == 3:
            self.loc = [self.loc[0] + 1, self.loc[1] + 1]
        elif direction == 4:
            self.loc = [self.loc[0] + 1, self.loc[1]]
        elif direction == 5:
            self.loc = [self.loc[0] + 1, self.loc[1] - 1]
        elif direction == 6:
            self.loc = [self.loc[0], self.loc[1] - 1]
        elif direction == 7:
            self.loc = [self.loc[0] - 1, self.loc[1] - 1]
        else:
            print("INVALID DIRECTION")

        # Reduce battery by the cost of movement or
        # don't move to invalid direction
        if math.inf in grid[self.loc[0]][self.loc[1]].get_costs():
            print("Staying put")
            self.loc = prev
        else:
            self.bat -= costs[direction]

        return self.loc[0], self.loc[1], prev[0], prev[1]

    def get_radius(self):
        return self.detection_radius

    def get_coords(self):
        return self.loc[0], self.loc[1]

    def get_bat(self):
        return self.bat