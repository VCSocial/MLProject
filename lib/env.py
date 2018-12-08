import numpy as np


class Env:

    def __init__(self, grid, max_fuel, start_x, start_y, flow_direction):

        self.dim_x = len(grid)
        self.dim_y = len(grid[0])

        # Initialize a 2D array to store the value of each cell
        # Give land cell the value 0, give water cell (unvisited) the value 1
        value = []

        for i in range(self.dim_x):
            value.append([])
            for j in range(self.dim_y):
                if grid[i][j] == 'O':
                    value[i].append(1)
                else:
                    value[i].append(0)

        self.shape = np.shape(grid)
        self.grid = grid
        self.value = value
        self.max_fuel = max_fuel
        self.fuel = max_fuel
        self.start_x = start_x
        self.start_y = start_y
        self.x = start_x
        self.y = start_y
        self.flow_direction = flow_direction

        print("Value: ", value)

    def value_update(self, a, b):

        if a >= self.dim_x or b >= self.dim_y:
            return

        if a < 0 or b < 0:
            return

        self.value[a][b] = self.value[a][b] - 0.5  #if self.value[a][b] - 0.2 > 0 else 0

    def step(self, action):
        # Get cell position after the "action"
        if action == 6 and self.grid[self.x][self.y - 1] == "O":
            self.y = self.y - 1

        if action == 5 and self.x + 1 < self.dim_x and self.y - 1 >= 0 and self.grid[self.x + 1][self.y - 1] == "O":
            self.x = self.x + 1
            self.y = self.y - 1

        if action == 4 and self.x + 1 < self.dim_x and self.grid[self.x + 1][self.y] == "O":
            self.x = self.x + 1

        if action == 3 and self.x + 1 < self.dim_x and self.y + 1 < self.dim_y and self.grid[self.x + 1][self.y + 1] == "O":
            self.x = self.x + 1
            self.y = self.y + 1

        if action == 2 and self.y + 1 < self.dim_y and self.grid[self.x][self.y + 1] == "O":
            self.y = self.y + 1

        if action == 1 and self.x - 1 >= 0 and self.y + 1 < self.dim_y and self.grid[self.x - 1][self.y + 1] == "O":
            self.x = self.x - 1
            self.y = self.y + 1

        if action == 0 and self.x - 1 >= 0 and self.grid[self.x - 1][self.y] == "O":
            self.x = self.x - 1

        if action == 7 and self.x - 1 >= 0 and self.y - 1 >= 0 and self.grid[self.x - 1][self.y - 1] == "O":
            self.x = self.x - 1
            self.y = self.y - 1

        x = self.x
        y = self.y

        # Update value of surrounding cells
        self.value_update(x, y + 1)
        self.value_update(x, y - 1)
        self.value_update(x + 1, y)
        self.value_update(x - 1, y)
        self.value_update(x + 1, y + 1)
        self.value_update(x - 1, y + 1)
        self.value_update(x + 1, y - 1)
        self.value_update(x - 1, y - 1)

        if x >= self.dim_x - 1 and y >= self.dim_y - 1:
            reward = self.value[x][y] + self.value[x][y - 1] + \
                     self.value[x - 1][y] + self.value[x - 1][y - 1]

        elif x >= self.dim_x - 1:
            reward = self.value[x][y] + self.value[x][y + 1] + self.value[x][y - 1] + \
                     self.value[x - 1][y] + self.value[x - 1][y + 1] + self.value[x - 1][y - 1]

        elif y >= self.dim_y - 1:
            reward = self.value[x][y] + self.value[x][y - 1] + self.value[x + 1][y] + \
                     self.value[x - 1][y] + self.value[x + 1][
                         y - 1] + self.value[x - 1][y - 1]
        else:
            reward = self.value[x][y] + self.value[x][y+1] + self.value[x][y-1] + self.value[x+1][y] + self.value[x-1][y] + self.value[x+1][y+1] + self.value[x-1][y+1] + self.value[x+1][y-1] + self.value[x-1][y-1]
            print("rewards:", self.value[x][y], self.value[x][y+1], self.value[x][y-1], self.value[x+1][y], self.value[x-1][y], self.value[x+1][y+1], self.value[x-1][y+1], self.value[x+1][y-1], self.value[x-1][y-1])

        # Update value of current cell
        self.value[x][y] = 0

        # This "next_state" is the state after "action"
        print("Next State: ", self.x, self.y)
        next_state = np.ravel_multi_index((self.x, self.y), self.shape)

        cost = np.abs(action - self.flow_direction)
        #cost = 1

        self.fuel = self.fuel - cost

        is_done = True if self.fuel <= 0 else False

        return next_state, reward, is_done

    def reset(self):
        value = []

        for i in range(len(self.grid)):
            value.append([])
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 'O':
                    value[i].append(1)
                else:
                    value[i].append(0)
        self.value = value
        self.x = self.start_x
        self.y = self.start_y
        self.fuel = self.max_fuel

        return np.ravel_multi_index((self.start_x, self.start_y), self.shape)
