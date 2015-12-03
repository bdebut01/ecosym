import threading
import sys
import random
from location import Location
from helper_functions import random_pick

class Organism(threading.Thread):
    def __init__(self, ecosystem, location=None):
        threading.Thread.__init__(self)
        if location is None:
            random.seed()
            i_loc = random.randint(0, ecosystem.hdim - 1) # these are inclusive
            j_loc = random.randint(0, ecosystem.vdim - 1)
            location = Location(i_loc, j_loc)
        self.location = location
        self.wasEaten = False
        self.lock = threading.Lock()
        self.directionXImpact = 0
        self.directionYImpact=0
        self.movementImpact=0 # this is actually "speed" 
        self.ecosystem = ecosystem
        self.timeCounter = ecosystem.globalTime
        self.survivalProbability = 0 # probability of surviving being eaten

    # calling (the built-in threading function) start on a thread runs the run()
    # function, so the actions we want the thread to run go in the run() func
    def run(self) :
        while True:
            self.ecosystem.barrier.wait()
            if self.wasEaten == True:
                self.die()
            self.performStandardAction()
    
    def performStandardAction(self):
        return
    #chooses a random direction to go
    #to be skipped if you have a more sophisticated movement algorithm
    def randomDirection(self):
        self.directionXImpact = random.uniform(-1,1)
        self.directionYImpact = random.uniform(-1,1)
    
    def move(self):
        newX = self.location.row+(self.directionXImpact*self.movementImpact)
        newY = self.location.col+(self.directionYImpact*self.movementImpact)
        self.ecosystem.moveOrganism(self, self.location, Location(newX, newY))
        self.loc=Location(newX, newY)
    
    def beEaten(self):
        self.wasEaten = random_pick([True, False], 
                [1 - self.survivalProbability, self.survivalProbability])
    
    def die(self):
        #if self.timeCounter != self.ecosystem.globalTime:
        #barrier push
        self.ecosystem.reportDeath(self)
        self.ecosystem.barrier.wait() # if we end the thread before calling
                                      # barrier.wait(), we'll have deadlock
        sys.exit() # Close this thread
    
    def printStatus(self):
        # depends on type of organism
        print "Testing"

