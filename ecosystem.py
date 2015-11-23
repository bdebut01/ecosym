from sets import Set
import location
from barrier import Barrier
from seablock import SeaBlock
from threading import Semaphore

class Ecosystem():
    def __init__(self, hdim, vdim):
        self.ocean = []
        self.globalTime=0
        self.barrier=Barrier(0)
        self.hdim = hdim
        self.vdim = vdim
        for i in range(hdim):
            row = []
            for j in range(vdim):
                tempblock = SeaBlock()
                row.append(tempblock)
            self.ocean.append(row)
        self.orgsList = Set()
    
    def loop(self):
        while True:
            # + 1 b/c barrier itself is being counted
            self.barrier.setN(len(self.orgsList)+1)
            self.barrier.wait()

    def moveOrganism(self, org, oldLoc, newLoc):
        #remove from oldLoc
        while int(newLoc.col < 0): #off west
            newLoc.col += vdim
        while int(newLoc.col) >= vdim: #off east
            newLoc.col -= vdim
        while int(newLoc.row < 0): #off north
            newLoc.row = 0-newLoc.row
            newLoc.col = newLoc.col + (hdim/2)
            if newLoc.col >= vdim:
                newLoc.col -= vdim
        while newLoc.row >= hdim: #off south
            newLoc.row = hdim-newLoc.row #over the pole
            newLoc.col = newLoc.col + (hdim/2)
            if newLoc.col >= vdim:
                newLoc.col -= vdim

    def printSimulation(self):
        # Loop through private organism set, calling their private print methods
        for org in self.orgsList:
            org.printStatus()

    def addOrganism(self, org, loc):
        self.getSeaBlock(loc).addOrganism(org)
        self.orgsList.add(org)
    
    def reportDeath(self, organism):
        organism.join()
        # remove from ocean block
        self.getSeaBlock(organism.location).removeOrganism(organism) 
        # remove from private organism list
        self.orgsList.remove(organism)

    def getSeaBlock(self, location):
        return self.ocean[int(location.row)][int(location.col)]
    
    
    def startSimulation(self) :
    # Automatically populating each seablock with an instance of coccolithophore
    for i in range(self.hdim):
        for j in range(self.vdim):
            temp = coccolithophores(location(i,j), self)
            self.addOrganism(temp, location(i,j))
    # start all organism threads
    # as in
    for org in self.orgsList :
        org.start()
    # Start infinite control loop
    loop() 


