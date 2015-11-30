import threading
import sys
import random
from location import Location

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
        self.movementImpact=0
        self.ecosystem = ecosystem
        self.timeCounter = ecosystem.globalTime

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
    
    def move(self):
        newX = self.location.row+(directionXImpact*movementImpact)
        newY = self.location.col+(directionYImpact*movementImpact)
        self.ecosystem.move(self.location, Location(newX, newY))
        self.loc=newLoc
    
    def beEaten(self):
        self.wasEaten = True
    
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

