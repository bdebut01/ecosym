import random
from organism import Organism
from fish import Fish

class Shark(Fish):
    def __init__(self, ecosystem, location = None, isNewborn = False):
        Fish.__init__(self, ecosystem, 20, location, isNewborn)
        self.survivalProbability = 1

    def reproduce(self):
        baby = Shark(self.ecosystem, self.location, True)
        self.ecosystem.addNewborn(baby)

    def printStatus(self):
        #print "Shark here"
        return
                

