class Vehicle:

    def __init__(self, bat=100, reg_data_rec=0, local_data_rec=0):
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
        self.loc = [0, 0]
        self.detection_radius = 1

    def move(self, direction):
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

        return self.loc[0], self.loc[1], prev[0], prev[1]

    def get_radius(self):
        return self.detection_radius

    def coords(self):
        return self.loc