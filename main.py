import sys
from ecosystem import Ecosystem
from seablock import SeaBlock
from location import Location

def main(argv):
    ecosystem = Ecosystem(10, 10)
    loc = Location(3,4)
    block = ecosystem.getSeaBlock(loc)
    block.printAttributes()

if __name__ == '__main__':
    main(sys.argv)

