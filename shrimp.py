import ecosystem
import seablock
import location
import random
from organism import Organism

class Shrimp(Organism):
    def __init__(self, ecosystem, location=None):
        Organism.__init__(self, ecosystem, location)
        self.population = 100
        self.hunger=50
    
    def performStandardAction(self):
        loc = self.ecosystem.getSeaBlock(self.location)
        localOrgs = loc.getOrganisms()
        prey = None
        for org in localOrgs:
            if self.ecosystem.isEdible(self, org):
                prey = org
                break
        #eat coccolithophores for each member of population
        food = 0
        if prey != None:
            for i in range(self.population):
                food = prey.beEaten()
                self.hunger -= (food/15000)
        #standard increase in hunger
        self.hunger += (self.population / 20)
        #reproduce
        self.movementImpact=food/20000
        if self.movementImpact < 0: self.movementImpact=0
        self.directionXImpact = random.uniform(-1,1)
        self.directionYImpact = random.uniform(-1,1)
        self.move()
        if self.hunger >= 100:
            self.hunger = 100
            self.population -= 1 #beginning to die of starvation
        if self.population <= 0:
            #print "Dying"
            self.die()
            #print "Died"
    
    def beEaten(self):
        self.population -= 1
        if self.population <= 0:
            self.wasEaten = True

    def printStatus(self):
        #print str(self.population) + " shrimp at ocean location (" + str(self.location.row) + ", " + str(self.location.col) + ")"
        return

