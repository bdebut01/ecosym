from sets import Set
import sys
from location import Location
from barrier import Barrier
from seablock import SeaBlock
from threading import Semaphore
from threading import Lock
from foodchain import Foodchain
from coccolithophores import Coccolithophores
from manatee import Manatee
from shrimp import Shrimp
from grouper import Grouper
from shark import Shark
from tuna import Tuna
from starfish import Starfish
from herring import Herring
from helper_functions import with_lock
import time
import graphic_output

global TICK_TIME

class Ecosystem():
    def __init__(self, simMins, hdim, vdim):
        self.simulationRunning = False
        self.maxSimTicks = simMins
        self.globalTicks = 0
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
        self.creatures = dict()
        self.creature_funcs = dict()
        global TICK_TIME
        TICK_TIME = 1 # we're waiting on sec
        self.stdoutLock = Lock()
    
    # Creates a 2D array of Seablocks with parameters passed in
    def createOcean(self, hdim, vdim):
        self.ocean = []
        for i in range(vdim):# vdim == rows
            row = []
            for j in range(hdim):# hdim == columns
                tempblock = SeaBlock()
                row.append(tempblock)
            self.ocean.append(row)
    
    # The "grass" of the ocean, the whole ocean is filled with
    #   coccolithophores, so prepopulate ocean with them in every block.
    def prepopulateCoccolithophores(self):
        # Automatically populating each seablock with an instance of coccolithophore
        for i in range(self.vdim):
            for j in range(self.hdim):
                plankton = Coccolithophores(self, Location(i,j))
                self.addOrganism(plankton)

    # Add new organism food chain relationships here.
    def createFoodchain(self):
        self.__foodchain = Foodchain()

        # we use types as keys and values
        self.__foodchain.addRelationship(Manatee, Coccolithophores)
        self.__foodchain.addMultiRelationship(Shark, [Manatee, Tuna, Starfish, 
            Grouper])
        self.__foodchain.addRelationship(Shrimp, Coccolithophores)
        self.__foodchain.addRelationship(Grouper, Shrimp)
        self.__foodchain.addMultiRelationship(Tuna, [Shrimp, Grouper, Herring])
        self.__foodchain.addRelationship(Starfish, Coccolithophores)
        self.__foodchain.addMultiRelationship(Herring, [Shrimp])

    def isEdible(self, predator, prey):
        """ Returns true if predator can eat prey. 
            Args:
            predator -- an instance of an Organism subclass
            prey -- an instance of an Organism subclass
        """
        return self.__foodchain.isEdible(type(predator), type(prey))

    def getNeighbors(self, org):
        """ Returns a list of organisms in the same SeaBlock as org. """
        return self.getSeaBlock(org.location).getOrganisms()

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
        newLoc.col = newLoc.col % self.hdim
        newLoc.row = newLoc.row % self.vdim 
        self.getSeaBlock(newLoc).addOrganism(org)
        return newLoc

    # Called in main to load the creatures the user typed in before the simulation
    #   starts running. 
    def loadCreatures(self, num_and_what_creatures, creature_funcs, creatures):
        self.creatures = creatures
        self.creature_funcs = creature_funcs
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
        print str(len(self.orgsList)) + " organisms alive"

    def addOrganism(self, org):
        self.getSeaBlock(org.location).addOrganism(org)
        with_lock(self.orgsListMutex, lambda : self.orgsList.add(org))

    def reportBirth(self, newborn):
        """ Notifies ecosystem that newborn was born 
            Args:
            newborn -- an instance of an Organism subclass
        """
        with_lock(self.newbornsMutex, lambda : self.newborns.append(newborn))
    
    def reportDeath(self, organism, reason):
        """ Notifies ecosystem that organism died
            Args:
            organism -- the instance of an Organism subclass that died
            reason -- reason for death as string
        """
        # remove from ocean block
        self.getSeaBlock(organism.location).removeOrganism(organism) 
        # remove from private organism list
        def remove():
            if organism in self.orgsList:
                self.orgsList.remove(organism)
        with_lock(self.orgsListMutex, remove)
        def printDeath():
            print "A " + type(organism).__name__.lower() + " died because: " + reason
        with_lock(self.stdoutLock, printDeath)

    def getSeaBlock(self, location):
        return self.ocean[int(location.row)][int(location.col)]
    
    def startSimulation(self):
        self.simulationRunning = True
        with_lock(self.orgsListMutex, lambda : self.barrier.setN(len(self.orgsList) + 1))

        # start all organism threads
        def startOrganisms():
            for org in self.orgsList:
                org.start()
        with_lock(self.orgsListMutex, startOrganisms)

        # Start infinite control loop
        self.loop() 
        sys.exit()

    def loop(self):
        divider = "-" * (54 + len(str(self.globalTicks)))
        print divider
        print "----------------------- Tick 0 ------------------------"
        print divider

        while self.simulationRunning:

            # sleep for TICK_TIME, so entire simulation has a normal heartbeat
            time.sleep(TICK_TIME)

            # after phase 1, all orgs should be done with actions, ecosystem 
            # can safely print status, do other maintenance
            self.barrier.phase1()
            # Print simulation for this tick, could embed this in a if i%amount == 0
            self.printSimulation()
            try:
                graphic_output.graphicsOutput(self.orgsList, "frame" + 
			str(self.globalTicks) +".jpg", self.hdim, self.vdim)
            except Exception:
                print "could not print this frame"
            
            self.addAndStartNewborns()
            with_lock(self.orgsListMutex, self.endSimulationIfNoOrganisms)

            # + 1 b/c ecosystem itself is being counted
            with_lock(self.orgsListMutex, lambda : self.barrier.setN(len(self.orgsList) + 1))

            self.globalTicks += 1
	    
	    # Print world stats every 10 ticks
            if self.globalTicks % 10 == 0:
                self.printRealStats()
	    
  	    # If exceed the number of ticks set by user initially, stop simulation
            if self.globalTicks >= self.maxSimTicks:
                self.simulationRunning = False

            if self.simulationRunning:
                divider = "-" * (54 + len(str(self.globalTicks)))
                print divider
                print "----------------------- Tick " + str(self.globalTicks)
		  + " ------------------------"
                print divider

            # reach barrier, allow everyone to go on to the next step
            self.barrier.phase2()

        print "------------------------------------------------------"
        print "------------------- Final Results --------------------"
        print "------------------------------------------------------"
        self.printRealStats()

	# End all threads
        def endThreads():
            for org in self.orgsList:
                org.join()
        with_lock(self.orgsListMutex, endThreads)

        return 

    def printRealStats(self):
        print '----- DEETS -----'
        for c in self.creature_funcs:
            counter = 0
            temp = self.creature_funcs[c]
            for org in self.orgsList:
                if type(org) == temp:
                    counter += 1
            print self.creatures[c] + " population: " + str(counter)
        print '-----------------'
        print ''

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
            self.reportDeath(thread, 'too many threads')

        # set the barrier again because if there were excess threads, n is incorrect
        with_lock(self.orgsListMutex, lambda : self.barrier.setN(len(self.orgsList) + 1))

        self.newborns = []

    # terrible name for a function but i can't think of anything better. might
    # refactor later.
    def endSimulationIfNoOrganisms(self):
        # if there are no organisms alive, simulation is over
        if len(self.orgsList) <= 0:
            print "No more organisms; ending simulation"
            self.simulationRunning = False

