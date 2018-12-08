from Simulator import osmparser
from lib import env
from Simulator.LearningAlgorithms import td_control
import numpy as np

class Train:

    def __init__(self, osm):
        # infile = './Data/map.xml'
        # o = osmparser.OSMParser(infile)
        grid, attrs = osm.retrieve_mapping()

        # Starting coordinates
        # self.x = 41
        # self.y = 19

        self.x = 41
        self.y = 19

        # Specify the start position to (41, 19), available fuel to be 100.
        environment = env.Env(grid, 100, self.x, self.y)

        # Train 100 episodes
        Q, stats = td_control.sarsa(environment, 1000, discount_factor=1, alpha=0.2, epsilon=0.1)
        shape = np.shape(grid)
        start_index = np.ravel_multi_index((self.x, self.y), shape)

        dim_x = len(grid)
        dim_y = len(grid[0])

        print(start_index)
        print(start_index // dim_x)
        print(start_index % dim_x)

        optimal_actions = []
        next_cell_index = start_index
        for i in range(99):
            action_values = Q[next_cell_index]
            optimal_action = np.argmax(action_values)
            optimal_actions.append(optimal_action)
            next_cell_index = self.next_state(next_cell_index, optimal_action, dim_x, dim_y, shape)

        # for i in range(99):
        #     action_values = Q[i]
        #     optimal_action = np.argmax(action_values)
        #     optimal_actions.append(optimal_action)

        #optimal_actions = [0, 1, 2, 3, 4, 5, 6, 7]

        print(stats.episode_lengths)
        print(stats.episode_rewards)
        print(optimal_actions)
        self.optimal_actions = optimal_actions

    def get_start(self):
        return self.x, self.y

    def retrieve_actions(self):
        return self.optimal_actions

    def next_state(self, cur_state, action, dim_x, dim_y, shp):
        x = cur_state // dim_x
        y = cur_state % dim_x

        if action == 6:
            y = y - 1

        if action == 5:
            x = x + 1
            y = y - 1

        if action == 4:
            x = x + 1

        if action == 3:
            x = x + 1
            y = y + 1

        if action == 2:
            y = y + 1

        if action == 1:
            x = x - 1
            y = y + 1

        if action == 0:
            x = x - 1

        if action == 7:
            x = x - 1
            y = y - 1

        if x < 0 or x > dim_x:
            x = cur_state // dim_x
        if y < 0 or y > dim_y:
            y = cur_state % dim_x
        print(x, y)
        return np.ravel_multi_index((x, y), shp)






