import numpy as np


class Env:

    def __init__(self, grid, max_fuel, start_x, start_y):

        # Initialize a 2D array to store the value of each cell
        # Give land cell the value 0, give water cell (unvisited) the value 1
        value = []

        for i in range(len(grid)):
            value.append([])
            for j in range(len(grid[0])):
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
        self.dim_x = len(grid)
        self.dim_y = len(grid[0])

    def value_update(self, a, b):

        if a >= len(self.grid) - 1 or b >= len(self.grid[0]) - 1:
            return

        if a < 0 or b < 0:
            return

        self.value[a][b] = self.value[a][b] - 0.5 if self.value[a][b] > 0.5 else 0

    def step(self, action):
        # Get cell position after the "action"
        if action == 0 and self.grid[self.x][self.y - 1] == "O":
            self.y = self.y - 1

        if action == 1 and self.x + 1 < self.dim_x and self.y - 1 >= 0 and self.grid[self.x + 1][self.y - 1] == "O":
            self.x = self.x + 1
            self.y = self.y - 1

        if action == 2 and self.x + 1 < self.dim_x and self.grid[self.x + 1][self.y] == "O":
            self.x = self.x + 1

        if action == 3 and self.x + 1 < self.dim_x and self.y + 1 < self.dim_y and self.grid[self.x + 1][self.y + 1] == "O":
            self.x = self.x + 1
            self.y = self.y + 1

        if action == 4 and self.y + 1 < self.dim_y and self.grid[self.x][self.y + 1] == "O":
            self.y = self.y + 1

        if action == 5 and self.x - 1 >= 0 and self.y + 1 < self.dim_y and self.grid[self.x - 1][self.y + 1] == "O":
            self.x = self.x - 1
            self.y = self.y + 1

        if action == 6 and self.x - 1 >= 0 and self.grid[self.x - 1][self.y] == "O":
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

        # Update value of current cell
        self.value[x][y] = 0

        # This "next_state" is the state after "action"
        print(self.x, self.y)
        next_state = np.ravel_multi_index((self.x, self.y), self.shape)

        self.fuel = self.fuel - 1

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
