import ecosystem
import seablock
import location

class Coccolithophores(Organism):
    def __init__(self, location, ecosystem):
        Organism.__init__(self, location, ecosystem)
        self.population = 1000000
    
    def performStandardAction(self):
        loc = self.ecosystem.getSeaBlock(self.location)
        population + (population * (1/loc.sunlight))
    
    def beEaten(Self):
        population = population - 15000
        if population <= 0:
            die()
    
