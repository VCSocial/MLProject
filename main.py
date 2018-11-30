# Project Specific
from Simulator.world import World

# General imports
import sys
import getopt
import os




def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["csv_file="])
    except getopt.GetoptError:
        print("Error parsing arguments! Exiting Now!")
        sys.exit(2)

    infile = ''
    for opt, arg in opts:
        if opt == '-h':
            print("Supply a CSV file for world generation with the flag -i")
        if opt == '-i':
            infile = arg

    if infile == '':
        print("Argument not supplied, default configuration loaded.")
        infile = './Data/map.xml'
        # ('./../Data/map.xml')

    print("Generating world from file:", infile)
    # Create the world

    world = World(infile)


    compass = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    # Traverse the world
    # world.traverse(compass.index('SE'))
    #world.traverse(compass.index('NW'))
    # world.pretty_print()
    world.navigate_with_policy()
    world.judgement_day()

    #Terminate execution
    os._exit(0)

if __name__ == "__main__":
    print("Tester")
    main(sys.argv[1:])

