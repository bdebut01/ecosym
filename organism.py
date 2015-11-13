
class Organism(threading.Thread):
    def __init__(self, location, ecosystem):
        threading.Thread.__init__(self)
        self.location = location
        self.lock = threading.Lock()
        self.ecosystem = ecosystem
    
    def performStandardAction(self):
        #sit there
    
    
    def move(self):
        #sit there
    
    def beEaten(self):
        die(self)
    
    def die(self):
        self.ecosystem.reportDeath(self)
