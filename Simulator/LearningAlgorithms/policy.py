import math
import random

class Policy:
    __LOGGING_LVL = 0
    __COMPASS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

    def __init__(self, algo="dumb"):
        print("Created")
        #self.dumb_and_gready()

    def random_move(self, pos=[], exploration_opts=[], coords=[]):

        while True:
            print("Flow in function")
            idx = random.randint(0, len(coords))
            print("Random index choosen:", idx)
            new_coord = coords[idx]
            print("New coordinates", new_coord)
            if new_coord[0] > 0 and new_coord[1] > 0:
                break

        move_dir = -1
        if pos[0] > new_coord[0] and pos[1] == new_coord[1]:
            move_dir = Policy.__COMPASS.index('N')
        if pos[0] > new_coord[0] and pos[1] < new_coord[1]:
            move_dir = Policy.__COMPASS.index('NE')
        if pos[0] == new_coord[0] and pos[1] < new_coord[1]:
            move_dir = Policy.__COMPASS.index('E')
        if pos[0] < new_coord[0] and pos[1] < new_coord[1]:
            move_dir = Policy.__COMPASS.index('SE')
        if pos[0] < new_coord[0] and pos[1] == new_coord[1]:
            move_dir = Policy.__COMPASS.index('S')
        if pos[0] > new_coord[0] and pos[1] < new_coord[1]:
            move_dir = Policy.__COMPASS.index('SW')

        if move_dir == -1:
            move_dir = Policy.__COMPASS.index('S')
        # INCOMPLETE MOVE SET
        if Policy.__LOGGING_LVL == 1:
            print("UAV moves:", Policy.__COMPASS[move_dir])

        return move_dir









