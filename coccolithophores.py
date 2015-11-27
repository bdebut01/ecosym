import ecosystem
import seablock
import location
from organism import Organism

class Coccolithophores(Organism):
    def __init__(self, ecosystem, location=None):
        Organism.__init__(self, ecosystem, location)
        self.population = 1000000
        self.virusWaxWane = -1 #starts waning strength virus
        self.virusEfficiency = 5000 #relatively weak
    
    def performStandardAction(self):
        loc = self.ecosystem.getSeaBlock(self.location)
        if loc.getSunlight() > 0:
            self.population += (self.population * (1/loc.getSunlight())) #reproduce photosynthetically
        
        ## commenting out virus stuff to simplify things until we get basic
        ## simulation working. just decreasing population by constant amount
        ## for now instead
        #self.population -= self.virusEfficiency
        #self.virusEfficiency += (self.virusWaxWane * (self.virusEfficiency/2)) #simple power-growth expand?
        #the tables turn
        #if self.virusEfficiency <= 100:
        #    self.virusWaxWane = 1
        #elif self.virusEfficiency >= 100000:
        #    self.virusWaxWane = -1
        self.population -= 20000

        #possible: affect viruses in adjacent cells?
        if self.population <= 0:
            print "Dying"
            self.die()
            print "Died"
    
    def beEaten(self):
        self.population -= 15000
        if self.population <= 0:
            print "Eaten"
            self.die()

    def printStatus(self):
        print self.ecosystem.getEdiblePreyTypes(str(type(self)))
        #print str(self.population) + " coccolithophores at ocean location (" + str(self.location.row) + ", " + str(self.location.col) + ")"

