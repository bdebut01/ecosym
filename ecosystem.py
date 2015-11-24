from sets import Set
from location import Location
from barrier import Barrier
from seablock import SeaBlock
from threading import Semaphore
from coccolithophores import Coccolithophores

import time

class Ecosystem():
    def __init__(self, hdim, vdim):
        self.ocean = []
        self.globalTime = 0
        self.barrier = Barrier(0)
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
        print "Before loop"
        while True:
            print "In loop"
            # probably sleep for TICK_TIME, so entire simulation has a normal heartbeat
            # time.sleep(TICK_TIME)
            # Print simulaiton for this tick, could embed this in a if i%amount == 0
            self.printSimulation()
            print len(self.orgsList) + 1
            # This belongs at end of whatever happens in this loop
            self.barrier.wait()
            # + 1 b/c barrier itself is being counted
            self.barrier.setN(len(self.orgsList) + 1)

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
            print "Printing org stats"
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
                                        # not sure about capitalized L for location, is this legal?
                temp = Coccolithophores(Location(i,j), self)
                print temp
                self.addOrganism(temp, Location(i,j))
        # start all organism threads
        # as in
        print len(self.orgsList) + 1
        self.barrier.setN(len(self.orgsList)+1)
        for org in self.orgsList :
            print "Starting an organism"
            org.start()
        # Start infinite control loop
        self.loop() 


