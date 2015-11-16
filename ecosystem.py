from sets import Set
import location
from seablock import SeaBlock

class Ecosystem():
    def __init__(self, hdim, vdim):
        self.ocean = []
        self.globalTime=0
        for i in range(hdim):
            row = []
            for j in range(vdim):
                tempblock = SeaBlock()
                row.append(tempblock)
            self.ocean.append(row)
        self.orgsList = Set()

    def addOrganism(self, org, loc):
        self.getSeaBlock(loc).addOrganism(org)
        self.orgsList.add(org)
    
    def reportDeath(self, organism):
        organism.join()
        self.orgsList.remove(organism)

    def getSeaBlock(self, location):
        return self.ocean[location.row][location.col]
    
    
    def run(self) :
        # start all organism threads
        # as in
        for org in self.orgsList() :
            org.start()