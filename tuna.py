import random
from organism import Organism
from fish import Fish

class Tuna(Fish):
    def __init__(self, ecosystem, location = None, isNewborn = False):
        Fish.__init__(self, ecosystem, 15, location)
        self.survivalProbability = .7

    def reproduce(self):
        newTuna = Tuna(self.ecosystem, self.location, True)
        self.ecosystem.addNewborn(newTuna)

    def printStatus(self):
        #print "Tuna here"
        return
                

