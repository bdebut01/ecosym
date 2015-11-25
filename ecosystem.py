from sets import Set
import sys
from location import Location
from barrier import Barrier
from seablock import SeaBlock
from threading import Semaphore
from threading import Lock
from coccolithophores import Coccolithophores

import time

def with_lock(lock, function):
    lock.acquire()
    try:
        value = function()
    finally:
        lock.release()

    return value


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
        self.orgsListMutex = Lock()
        self.prepopulateCoccolithophores()

    def prepopulateCoccolithophores(self):
        # Automatically populating each seablock with an instance of coccolithophore
        for i in range(self.hdim):
            for j in range(self.vdim):
                temp = Coccolithophores(Location(i,j), self)
                self.addOrganism(temp, Location(i,j))

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
        def print_orgs():
            for org in self.orgsList:
                org.printStatus()
        with_lock(self.orgsListMutex, print_orgs)

    def addOrganism(self, org, loc):
        self.getSeaBlock(loc).addOrganism(org)
        with_lock(self.orgsListMutex, lambda : self.orgsList.add(org))
    
    def reportDeath(self, organism):
        #organism.join()
        # remove from ocean block
        self.getSeaBlock(organism.location).removeOrganism(organism) 
        # remove from private organism list
        with_lock(self.orgsListMutex, lambda : self.orgsList.remove(organism))
        print "Death reported"

    def getSeaBlock(self, location):
        return self.ocean[int(location.row)][int(location.col)]
    
    def startSimulation(self):
        with_lock(self.orgsListMutex, lambda : self.barrier.setN(len(self.orgsList)+1))
        #self.barrier.setN(len(self.orgsList)+2) # adding two so that simulation stops after one time step, for testing

        # start all organism threads
        def startOrganisms():
            for org in self.orgsList:
                org.start()
        with_lock(self.orgsListMutex, startOrganisms)

        # Start infinite control loop
        self.loop() 

    def loop(self):
        self.__simulationRunning = True  # making this a member variable so that
                                         # it can be easily accessed within the
                                         # end_simulation function defined below
        while self.__simulationRunning:
            print "-----------------------In loop------------------------"
            # probably sleep for TICK_TIME, so entire simulation has a normal heartbeat
            # time.sleep(TICK_TIME)

            # after phase 1, all orgs should be done with actions, ecosystem 
            # can safely print status, do other maintenance
            self.barrier.phase1()
            # Print simulaiton for this tick, could embed this in a if i%amount == 0
            self.printSimulation()

            with_lock(self.orgsListMutex, self.endSimulationIfNoOrganisms)
            if self.__simulationRunning:
                # + 1 b/c barrier itself is being counted
                with_lock(self.orgsListMutex, lambda : self.barrier.setN(len(self.orgsList) + 1))

            # reach barrier, allow everyone to go on to the next step
            self.barrier.phase2()

    # Used for debugging purposes
    def printNumOrgs(self):
        print len(self.orgsList) + 1

    # terrible name for a function but i can't think of anything better. might
    # refactor later.
    def endSimulationIfNoOrganisms(self):
        # if there are no organisms alive, simulation is over
        print len(self.orgsList)
        if len(self.orgsList) <= 0:
            print "Ending simulation"
            self.__simulationRunning = False

