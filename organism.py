import threading

class Organism(threading.Thread):
    def __init__(self, location, ecosystem):
        threading.Thread.__init__(self)
        self.location = location
        self.lock = threading.Lock()
        self.ecosystem = ecosystem
        self.timeCounter = ecosystem.globalTime

    def run(self) :
        while True:
            self.performStandardAction()
            self.ecosystem.barrier.wait()
        # while(1)
            # do things
            # performStandardAction()
            # barrier.wait()
    
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
        self.exit() # Close this thread
    
    def printStatus(self):
        # depends on type of organism
        print "Testing"

