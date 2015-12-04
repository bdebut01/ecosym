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
            row = random.randint(0, ecosystem.vdim - 1) # these are inclusive
            col = random.randint(0, ecosystem.hdim - 1)
            location = Location(row, col)
        self.location = location
        self.wasEaten = False
        self.lock = threading.Lock()
        self.directionXImpact = 0
        self.directionYImpact=0
        self.movementImpact=0 # this is actually "speed" 
        self.ecosystem = ecosystem
        self.timeCounter = ecosystem.globalTicks
        self.survivalProbability = 0 # probability of surviving being eaten

    # calling (the built-in threading function) start on a thread runs the run()
    # function, so the actions we want the thread to run go in the run() func
    def run(self) :
        while True:
            self.ecosystem.barrier.wait()
            if self.wasEaten == True:
                self.die('eaten!')
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
        self.location=self.ecosystem.moveOrganism(self, self.location, Location(newX, newY))
    
    def beEaten(self):
        self.wasEaten = random_pick([True, False], 
                [1 - self.survivalProbability, self.survivalProbability])
    
    def die(self, reason):
        #if self.timeCounter != self.ecosystem.globalTicks:
        #barrier push
        self.ecosystem.reportDeath(self, reason)
        self.ecosystem.barrier.wait() # if we end the thread before calling
                                      # barrier.wait(), we'll have deadlock
        sys.exit() # Close this thread
    
    def printStatus(self):
        # depends on type of organism
        print "Testing"

