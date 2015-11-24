import ecosystem
import seablock
import location
from organism import Organism

class Coccolithophores(Organism):
    def __init__(self, location, ecosystem):
        Organism.__init__(self, location, ecosystem)
        self.population = 1000000
        self.virusWaxWane = -1 #starts waning strength virus
        self.virusEfficiency = 5000 #relatively weak
    
    def performStandardAction(self):
        loc = self.ecosystem.getSeaBlock(self.location)
        if loc.getSunlight() > 0:
            self.population += (self.population * (1/loc.getSunlight())) #reproduce photosynthetically
        
        self.population -= self.virusEfficiency
        self.virusEfficiency += (self.virusWaxWane * (self.virusEfficiency/2)) #simple power-growth expand?
        #the tables turn
        if self.virusEfficiency <= 100:
            self.virusWaxWane = 1
        elif self.virusEfficiency >= 100000:
            self.virusWaxWane = -1

        #possible: affect viruses in adjacent cells?
        if (self.population <= 0):
            die()
    
    def beEaten(self):
        population = population - 15000
        if population <= 0:
            die()

    def printStatus(self):
        print self.population

