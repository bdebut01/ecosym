from sets import Set
import sys
from location import Location
from barrier import Barrier
from seablock import SeaBlock
from threading import Semaphore
from threading import Lock
from foodchain import Foodchain
from coccolithophores import Coccolithophores
from bulbasaur        import Bulbasaur
from manatee import Manatee
from shrimp import Shrimp
from shark import Shark
from tuna import Tuna
from helper_functions import with_lock
import time

global TICK_TIME

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
        self.newborns = []
        self.newbornsMutex = Lock()
        global TICK_TIME
        TICK_TIME = 1 # we're waiting on sec
    
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


    def createFoodchain(self):
        # this is an example, we should change this as soon as we have actual
        # predators and prey
        self.__foodchain = Foodchain()
        self.__foodchain.addRelationship(Bulbasaur, Coccolithophores)
        self.__foodchain.addRelationship(Manatee, Coccolithophores)
        self.__foodchain.addRelationship(Shark, Manatee)
        self.__foodchain.addRelationship(Shrimp, Coccolithophores)
        self.__foodchain.addRelationship(Shark, Tuna)

    # tells you if the predator can eat the potential prey (note: pass in an
    # an instance of an organism subclass. 
    # e.g. myShark = Shark(...)
    #      myFish = Fish(...)
    #      isEdible(myShark, myFish) # should return True
    def isEdible(self, predator, prey):
        return self.__foodchain.isEdible(type(predator), type(prey))

    def moveOrganism(self, org, oldLoc, newLoc):
        #remove from oldLoc
        self.getSeaBlock(oldLoc).removeOrganism(org)
        while int(newLoc.col < 0): #off west
            newLoc.col += self.vdim
        while int(newLoc.col) >= self.vdim: #off east
            newLoc.col -= self.vdim
        while int(newLoc.row < 0): #off north
            newLoc.row = 0-newLoc.row
            newLoc.col = newLoc.col + (self.hdim/2)
            if newLoc.col >= self.vdim:
                newLoc.col -= self.vdim
        while newLoc.row >= self.hdim: #off south
            newLoc.row = self.hdim-newLoc.row #over the pole
            newLoc.col = newLoc.col + (self.hdim/2)
            if newLoc.col >= self.vdim:
                newLoc.col -= self.vdim
        newLoc.col = newLoc.col % hdim
        newLoc.row = newLoc.row % vdim 
        self.getSeaBlock(newLoc).addOrganism(org)
        return newLoc

    # Called in main to load the creatures the user typed in before the simulation
    #   starts running. 
    def loadCreatures(self, num_and_what_creatures, creature_funcs):
        # Loop thru num_and_what_creatures dictionary for which species and quantities
        for key in num_and_what_creatures:
            for i in range(num_and_what_creatures[key]): # for every creature of that species
                # Instantiate organism using creature function dict, no location passed
                #   so random will be chosen by constructor
                newOrganism = creature_funcs[int(key)](self)
                self.addOrganism(newOrganism)

    def printSimulation(self):
        # Loop through private organism set, calling their print methods
        def print_orgs():
            for org in self.orgsList:
                org.printStatus()
        with_lock(self.orgsListMutex, print_orgs)

    def addOrganism(self, org):
        self.getSeaBlock(org.location).addOrganism(org)
        with_lock(self.orgsListMutex, lambda : self.orgsList.add(org))

    def addNewborn(self, newborn):
        with_lock(self.newbornsMutex, lambda : self.newborns.append(newborn))
    
    def reportDeath(self, organism, reason):
        # remove from ocean block
        self.getSeaBlock(organism.location).removeOrganism(organism) 
        # remove from private organism list
        def remove():
            if organism in self.orgsList:
                self.orgsList.remove(organism)
        with_lock(self.orgsListMutex, remove)
        if type(organism) != Coccolithophores:
            print "A " + str(type(organism)) + " died because: " + reason

    def getSeaBlock(self, location):
        print "row"
        print location.row
        print int(location.row)
        print "hdim" + str(self.hdim)
        print "col"
        print location.col
        print int(location.col)
        print "vdim" + str(self.vdim)
        return self.ocean[int(location.row)][int(location.col)]
    
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
            time.sleep(TICK_TIME)

            # after phase 1, all orgs sould be done with actions, ecosystem 
            # can safely print status, do other maintenance
            self.barrier.phase1()
            # Print simulation for this tick, could embed this in a if i%amount == 0
            self.printSimulation()

            self.addAndStartNewborns()
            # + 1 b/c barrier itself is being counted
            with_lock(self.orgsListMutex, lambda : self.barrier.setN(len(self.orgsList) + 1))
            with_lock(self.orgsListMutex, self.endSimulationIfNoOrganisms)
            print "Entering phase 2"
            # reach barrier, allow everyone to go on to the next step
            self.barrier.phase2()

    def addAndStartNewborns(self):
        for newborn in self.newborns:
            self.addOrganism(newborn)

        # need to set barrier's n before starting threads so that they immediately block
        with_lock(self.orgsListMutex, lambda : self.barrier.setN(len(self.orgsList) + 1))

        excessThreads = []
        def startThreadsUpToLimit():
            for org in self.orgsList:
                if not org.isAlive():
                    try:
                        org.start()
                    except Exception as e:
                        excessThreads.append(org)
        with_lock(self.orgsListMutex, startThreadsUpToLimit)

        # if we've reached the thread limit, some newborns don't get to live
        for thread in excessThreads:
            self.reportDeath(thread)

        # set the barrier again because if there were excess threads, n is incorrect
        with_lock(self.orgsListMutex, lambda : self.barrier.setN(len(self.orgsList) + 1))

        self.newborns = []


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

