class coccolithophores(organism):
    def __init__(self, location, ecosystem):
        organism.__init__(self, location, ecosystem)
        self.population = 1000000
    
    def performStandardAction(self):
        loc = self.ecosystem.getLocation(self.location)
        population + (population * (1/loc.sunlight))
    
    def beEaten(Self):
        population = population - 15000
        if population <= 0:
            die()
    