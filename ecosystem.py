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
from shark import Shark
from tuna import Tuna
from thread_functions import with_lock
import time
import random

class Ecosystem():
    def __init__(self, hdim, vdim):
        self.globalTime = 0
        self.barrier = Barrier(0)
        self.hdim = hdim
        self.vdim = vdim
        self.orgsList = Set()
        self.orgsListMutex = Lock()
        self.createOcean(hdim, vdim)
        #self.prepopulateCoccolithophores()
        self.createFoodchain()
        self.newborns = []
        self.newbornsLock = Lock()
    
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
                if org.isAlive():
                    org.printStatus()
        with_lock(self.orgsListMutex, print_orgs)

    def addOrganism(self, org):
        self.getSeaBlock(org.location).addOrganism(org)
        with_lock(self.orgsListMutex, lambda : self.orgsList.add(org))

    def addNewborn(self, newborn):
        with_lock(self.newbornsLock, lambda : self.newborns.append(newborn))
    
    def reportDeath(self, organism):
        # remove from ocean block
        self.getSeaBlock(organism.location).removeOrganism(organism) 
        # remove from private organism list
        def remove():
            self.orgsList.discard(organism)
        with_lock(self.orgsListMutex, remove)
        #if type(organism) != Coccolithophores:
        #    print str(type(organism)) + "Death reported"

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

            print "Value of barrier: " + str(self.barrier.n)
            print "Len of orgs list before starting newborns: " + str(len(self.orgsList))
            def startNewborns():
                i = 0
                j = 0
                for org in self.orgsList:
                    if not org.isAlive():
                        org.start()
                        i += 1
                    else:
                        j += 1
                print "started " + str(i)
                print "already active " + str(j)
            with_lock(self.orgsListMutex, startNewborns)

            # after phase 1, all orgs should be done with actions, ecosystem 
            # can safely print status, do other maintenance
            print "done phase 1"
            self.barrier.phase1()
            print "def done phase 1"
            # Print simulaiton for this tick, could embed this in a if i%amount == 0
            self.printSimulation()

            if len(self.orgsList) + len(self.newborns) >= 1500:
                numOrgsToRemove = random.randint(200, 300)
                numNewbornsToRemove = random.randint(0, len(self.newborns) / 2)
                if len(self.newborns) - numNewbornsToRemove > 200:
                    numNewbornsToRemove = len(self.newborns) - 200

                while len(self.orgsList) >= 1700:
                    org = self.orgsList.pop()
                    self.orgsList.add(org)
                    self.reportDeath(org)

                for i in range(numOrgsToRemove):
                    org = self.orgsList.pop()
                    self.orgsList.add(org)
                    self.reportDeath(org)

                for i in range(numNewbornsToRemove):
                    self.newborns.pop()
                print "Threads reduced"
                    
            for i in range(len(self.newborns)):
                org = self.newborns.pop()
                self.addOrganism(org)
                #org.start()
                if i == 0:
                    print str(len(self.newborns)) + " Babies added"

            # + 1 b/c barrier itself is being counted
            with_lock(self.orgsListMutex, lambda : self.barrier.setN(len(self.orgsList) + 1))
            print "set barrier to " + str(self.barrier.n)
            self.newborns = []
            with_lock(self.orgsListMutex, self.endSimulationIfNoOrganisms)
            # reach barrier, allow everyone to go on to the next step
            self.barrier.phase2()
            print "After phase 2"

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
        else:
            print "Not ending sim"

