from sets import Set
import sys
from location import Location
from barrier import Barrier
from seablock import SeaBlock
from threading import Semaphore
from threading import Lock
from coccolithophores import Coccolithophores
from bulbasaur        import Bulbasaur

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
        self.globalTime = 0
        self.barrier = Barrier(0)
        self.hdim = hdim
        self.vdim = vdim
        self.orgsList = Set()
        self.orgsListMutex = Lock()
        self.createOcean(hdim, vdim)
        self.prepopulateCoccolithophores()
        self.createFoodchain()
    
    def createOcean(self, hdim, vdim):
        self.ocean = []
        for i in range(hdim):
            row = []
            for j in range(vdim):
                tempblock = SeaBlock()
                row.append(tempblock)
            self.ocean.append(row)

    def prepopulateCoccolithophores(self):
        # Automatically populating each seablock with an instance of coccolithophore
        for i in range(self.hdim):
            for j in range(self.vdim):
                plankton = Coccolithophores(self, Location(i,j))
                self.addOrganism(plankton)

    # creates a dictionary where the keys and vals are organism subclass
    # types. The keys represent the "predators" and the
    # vals are lists of the "prey" they can eat. e.g. it could tell you that
    # a shark can eat a fish. that would look something like this:
    # { <type 'shark.Shark'>: [<type 'fish.Fish'>] }
    def createFoodchain(self):
        # this is an example, we should change this as soon as we have actual
        # predators and prey
        self.__foodchain = { str(Coccolithophores): [str(Coccolithophores)] }

    # tells you if the predator can eat the potential prey (note: pass in an
    # an instance of an organism subclass. 
    # e.g. myShark = Shark(...)
    #      myFish = Fish(...)
    #      isEdible(myShark, myFish) # should return True
    def isEdible(self, predator, prey):
        predTy = type(predator)
        preyTy = type(prey)
        if predTy in self.__foodchain and preyTy in self.__foodchain[predTy]:
            return True
        else:
            return False

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

    def loadCreatures(self, num_and_what_creatures, creature_funcs):
        # Loop thru num_and_what_creatures dictionary for which and quantities
        for key in num_and_what_creatures:
            for i in num_and_what_creatures[key]: # for every creature of that species
                # Instantiate organism using creature function dict, no location passed
                #   so random will be chosen by constructor
                temp_func = creature_funcs[int(key)]
                newOrganism = temp_func(self)
                self.addOrganism(newOrganism)
                break

    def printSimulation(self):
        # Loop through private organism set, calling their print methods
        def print_orgs():
            for org in self.orgsList:
                org.printStatus()
        with_lock(self.orgsListMutex, print_orgs)

    def addOrganism(self, org):
        self.getSeaBlock(org.location).addOrganism(org)
        with_lock(self.orgsListMutex, lambda : self.orgsList.add(org))
    
    def reportDeath(self, organism):
        # remove from ocean block
        self.getSeaBlock(organism.location).removeOrganism(organism) 
        # remove from private organism list
        with_lock(self.orgsListMutex, lambda : self.orgsList.remove(organism))
        print "Death reported"

    def getSeaBlock(self, location):
        return self.ocean[location.row][location.col]
    
    def startSimulation(self):
        with_lock(self.orgsListMutex, lambda : self.barrier.setN(len(self.orgsList) + 1))

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

