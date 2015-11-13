from sets import Set
import location
import seablock

class Ecosystem():
    def __init__(self, hdim, vdim):
        self.ocean = []
        for i in range(hdim):
            row = []
            for j in range(vdim):
                tempblock = SeaBlock()
                row[j] = tempblock
            self.ocean[i] = row
        self.orgsList = Set()

    def reportDeath(self, organism):
        organism.join()
        self.orgsList.remove(organism)

    def getSeaBlock(location):
        return self.ocean[location.row][location.col]
    
    
