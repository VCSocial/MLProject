from Simulator import osmparser
from lib import env
from Simulator.LearningAlgorithms import td_control
import numpy as np


infile = './Data/map.xml'
o = osmparser.OSMParser(infile)
grid, attrs = o.retrieve_mapping()

# Specify the start position to (41, 19), available fuel to be 100.
environment = env.Env(grid, 100, 41, 19)

# Train 100 episodes
Q, stats = td_control.sarsa(environment, 100)
shape = np.shape(grid)
start_index = np.ravel_multi_index((41, 19), shape)

dim_x = len(grid)
dim_y = len(grid[0])

print(start_index)
print(start_index // dim_x)
print(start_index % dim_x)


def next_state(cur_state, action):
    x = cur_state // dim_x
    y = cur_state % dim_x

    if action == 0:
        y = y - 1

    if action == 1:
        x = x + 1
        y = y - 1

    if action == 2:
        x = x + 1

    if action == 3:
        x = x + 1
        y = y + 1

    if action == 4:
        y = y + 1

    if action == 5:
        x = x - 1
        y = y + 1

    if action == 6:
        x = x - 1

    if action == 7:
        x = x - 1
        y = y - 1

    if x < 0 or x > dim_x:
        x = cur_state // dim_x
    if y < 0 or y > dim_y:
        y = cur_state % dim_x
    print(x, y)
    return np.ravel_multi_index((x, y), shape)


optimal_actions = []
next_cell_index = start_index
for i in range(99):
    action_values = Q[next_cell_index]
    optimal_action = np.argmax(action_values)
    optimal_actions.append(optimal_action)
    next_cell_index = next_state(next_cell_index, optimal_action)


print(stats.episode_lengths)

print(optimal_actions)



