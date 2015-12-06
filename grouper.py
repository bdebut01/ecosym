import random
from organism import Organism
from fish import Fish

class Grouper(Fish):
    def __init__(self, ecosystem, location = None, isNewborn = False):
        Fish.__init__(self, ecosystem, 3, 1, location)
        self.survivalProbability = .4
        self.movementImpact = .4

    def reproduce(self):
        newTuna = Tuna(self.ecosystem, self.location, True)
        self.ecosystem.addNewborn(newTuna)

    def printStatus(self):
        #print "Tuna here"
        # print "Tuna at " + str(self.location.row) + ", " + str(self.location.col)
        return
                

