#organism module
#the general superclass for all organisms in the simulation
#Part of the EcoSym Project

import threading
import sys
import random
from location import Location
from helper_functions import random_pick
from helper_functions import with_lock

#this class represents one organism of some type
#it includes two major components:
#1. Functions for general initialization and running of an organism
#and handling the concurrent nature of the organisms (which are also threads)
#2. Functions useful for most if not all organisms
#that are commonly used in most subclasses

class Organism(threading.Thread):
    #creates an organism
    #given the host ecosystem
    #and an optional location (useful if the creature is a newborn or specifically placed)
    #if no location is provided, the organism will be randomly placed
    def __init__(self, ecosystem, location=None):
        threading.Thread.__init__(self)
        if location is None: # If called w/o specific location,
			     # give random
            random.seed() # These seed is actually globally important
            row = random.randint(0, ecosystem.vdim - 1) # these are inclusive
            col = random.randint(0, ecosystem.hdim - 1)
            location = Location(row, col)
        self.location = location
        self.wasEaten = False
        self.beEatenLock = threading.Lock()
        #variables for motion
        #the direction impacts mark the orientation of the creature and should be between -1 and 1
        #the movement impact is the speed of the creature and should logically be positive
        #although negative speeds and high/low directions will be calculated without errors
        self.directionXImpact = 0
        self.directionYImpact=0
        self.movementImpact=0 # this is actually "speed" 
        self.ecosystem = ecosystem
        self.survivalProbability = 0 # probability of surviving being eaten

    # calling (the built-in threading function) start on a thread runs the run()
    # function, so the actions we want the thread to run go in the run() func
    def run(self) :
        while self.ecosystem.simulationRunning == True:
            self.ecosystem.barrier.wait()
            if self.ecosystem.simulationRunning == False: # in case sim ended while thread was blocked
                break
            if self.wasEaten == True:
                self.die('eaten!')
            self.performStandardAction()
    
    # To be filled out by every inheriting organism
    def performStandardAction(self):
        return
    
    # chooses a random direction to face
    # 	to be overwritten if you have a more sophisticated movement algorithm
    def randomDirection(self):
        self.directionXImpact = random.uniform(-1,1)
        self.directionYImpact = random.uniform(-1,1)
    
    # Using previously-set direction variables, move self in that direction
    def move(self):
        newX = self.location.row+(self.directionXImpact*self.movementImpact)
        newY = self.location.col+(self.directionYImpact*self.movementImpact)
        self.location=self.ecosystem.moveOrganism(self, self.location, Location(newX, newY))
    
    #beEaten is called by predators to attempt to consume this organism
    #it returns data based on success or failure of the attempt
    def beEaten(self):
        def getEaten():
            if not self.wasEaten: # in case we've already been eaten
                self.wasEaten = random_pick([True, False], 
                        [1 - self.survivalProbability, self.survivalProbability])
                return self.wasEaten
            else:
                return False # though you were eaten, the org calling beEaten wasn't the one who ate you
        return with_lock(self.beEatenLock, getEaten)
    
    #to handle the death of the organism
    #this function is meant only to be called internally
    def die(self, reason):
        # barrier push
        self.ecosystem.reportDeath(self, reason)
        self.ecosystem.barrier.wait() # if we end the thread before calling
                                      # barrier.wait(), we'll have deadlock
        sys.exit() # Close this thread
    
    #a debug function to print data from this organism
    #also used for output to the user
    def printStatus(self):
        # depends on type of organism
        print "Testing"



