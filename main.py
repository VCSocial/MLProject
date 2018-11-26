# Project Specific
from Simulator.genworld import GenWorld
from Simulator.osmparser import OSMParser

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
        infile = './Data/20180425_154714_Initial_scan_1may17_IVER2-218.csv'

    print("Generating world from file:", infile)
    # Create the world

    world = GenWorld(infile)


    compass = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    # Traverse the world
    #world.traverse(compass.index('SE'))
    #world.traverse(compass.index('S'))
    # world.pretty_print()
    world.navigate_with_policy()
    world.judgement_day()

    #Terminate execution
    os._exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])

