import math
import random

class Policy:
    __LOGGING_LVL = 1
    __COMPASS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

    def __init__(self, algo="dumb"):
        print("Beginning to nvaigate by policy")

    def get_dir(self, pos, new_coord):
        move_dir = -1

        if pos[0] == new_coord[0] and pos[1] > new_coord[1]:
            move_dir = Policy.__COMPASS.index('N')
        if pos[0] < new_coord[0] and pos[1] > new_coord[1]:
            move_dir = Policy.__COMPASS.index('NE')
        if pos[0] < new_coord[0] and pos[1] == new_coord[1]:
             move_dir = Policy.__COMPASS.index('E')
        if pos[0] < new_coord[0] and pos[1] < new_coord[1]:
            move_dir = Policy.__COMPASS.index('SE')
        if pos[0] == new_coord[0] and pos[1] < new_coord[1]:
            move_dir = Policy.__COMPASS.index('S')
        if pos[0] > new_coord[0] and pos[1] < new_coord[1]:
            move_dir = Policy.__COMPASS.index('SW')
        if pos[0] > new_coord[0] and pos[1] == new_coord[1]:
            move_dir = Policy.__COMPASS.index('W')
        if pos[0] > new_coord[0] and pos[1] > new_coord[1]:
             move_dir = Policy.__COMPASS.index('NW')

        if move_dir == -1:
            print(">>>>>>>>> INVALID MOVE")
            print(">>>>>>>>>", pos, new_coord)
            move_dir = Policy.__COMPASS.index('S')

        # INCOMPLETE MOVE SET
        if Policy.__LOGGING_LVL == 1:
            print(">>>>>>>>>", pos, new_coord)
            print(">>>>>>>>> UAV MOVES:", Policy.__COMPASS[move_dir])

        return move_dir

    def random_move(self, pos=[], exploration_opts=[], coords=[]):

        # Randomly and unintelligently pick a direction to move in
        while True:
            idx = random.randint(0, len(coords) - 1)
            new_coord = coords[idx]

            if Policy.__LOGGING_LVL == 1:
                print("Random index choosen:", idx)
                print("New coordinates", new_coord)

            if new_coord[0] > 0 and new_coord[1] > 0:
                break

        return self.get_dir(pos, new_coord)









