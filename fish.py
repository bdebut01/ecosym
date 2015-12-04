import random
from organism import Organism

class Fish(Organism):
    def __init__(self, ecosystem, lifespanYears, maturityYears, location = None, isNewborn = False):
        Organism.__init__(self, ecosystem, location)
        if random.randint(0, 1) == 0:
            self.sex = "M"
        else:
            self.sex = "F"

        self.lifespanTicks = lifespanYears * 365 * 24 * 60 # years * days * hours * mins
        self.maturityTicks = maturityYears * 365 * 24 * 60

        if isNewborn:
            self.ticksAlive = 0
        else:
            self.ticksAlive = random.randint(0, self.lifespanTicks - 1)

        self.hunger = 10 # going to starve after 20
        self.isMature = self.ticksAlive >= self.maturityTicks

    def performStandardAction(self):
        if self.ticksAlive >= self.lifespanTicks:
            self.die('old age!') # die of old age

        if self.isMature == False and self.ticksAlive >= self.maturityTicks:
            self.isMature = True

        myBlock = self.ecosystem.getSeaBlock(self.location)
        neighborOrgs = myBlock.getOrganisms()
        for org in neighborOrgs:
            if type(org) == type(self): # found a fellow shark!
                if self.isMature and org.sex != self.sex and org.isMature:
                    self.reproduce()
                    break
            elif self.ecosystem.isEdible(self, org):
                org.beEaten()
                self.hunger -= 1
                break
        if self.hunger > 20:
            self.die('starvation!')
        self.hunger += 1 # every tick get 1 more hunger unit
        self.randomDirection()
        self.move()
        self.ticksAlive += 1

    def printStatus(self):
        # print "Shark at location " + str(self.location.row) + ", " + str(self.location.col)
        #print "Shark here"
        return
                


