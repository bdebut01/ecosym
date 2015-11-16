
class Organism(threading.Thread):
    def __init__(self, location, ecosystem):
        threading.Thread.__init__(self)
        self.location = location
        self.lock = threading.Lock()
        self.ecosystem = ecosystem
        self.timeCounter = ecosystem.globalTime

    def start(self) :
        # start doing things
    
    def performStandardAction(self):
        #sit there
    
    
    def move(self):
        #sit there
    
    def beEaten(self):
        die(self)
    
    def die(self):
        if self.timeCounter != self.ecosystem.globalTime:
        #barrier push
        self.ecosystem.reportDeath(self)
        self.exit() # Close this thread
