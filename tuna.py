import random
from organism import Organism

class Tuna(Organism):
    def __init__(self, ecosystem, location = None):
        Organism.__init__(self, ecosystem, location)
        if random.randint(0, 1) == 0:
            self.sex = "M"
        else:
            self.sex = "F"

        self.ticksAlive = 0
        self.lifespanTicks = 15 * 365 * 24 * 60 # years * days * hours * mins

    def performStandardAction(self):
        if self.ticksAlive >= self.lifespanTicks:
            self.die() # die of old age

        myBlock = self.ecosystem.getSeaBlock(self.location)
        neighborOrgs = myBlock.getOrganisms()
        for org in neighborOrgs:
            if type(org) == type(self): # found a fellow tuna!
                if org.sex != self.sex:
                    self.reproduce()
                    break
            elif self.ecosystem.isEdible(self, org):
                org.beEaten()
                break
        self.ticksAlive += 1

    def reproduce(self):
        newTuna = Tuna(self.ecosystem, self.location)
        self.ecosystem.addNewborn(newTuna)

    def printStatus(self):
        #print "Tuna here"
        return
                

