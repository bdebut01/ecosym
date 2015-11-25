import threading
import sys

class Organism(threading.Thread):
    def __init__(self, location, ecosystem):
        threading.Thread.__init__(self)
        self.location = location
        self.lock = threading.Lock()
        self.ecosystem = ecosystem
        self.timeCounter = ecosystem.globalTime

    # calling (the built-in threading function) start on a thread runs the run()
    # function, so the actions we want the thread to run go in the run() func
    def run(self) :
        while True:
            self.ecosystem.barrier.wait()
            self.performStandardAction()
    
    def performStandardAction(self):
        #sit there
        return
    
    def move(self):
        #sit there
        return
    
    def beEaten(self):
        self.die(self)
    
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

