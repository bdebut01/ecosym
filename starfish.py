import random
from organism import Organism

class Starfish(Organism):
    def __init__(self, ecosystem, location = None, isNewborn = False):
        Organism.__init__(self, ecosystem, location)
        self.lifespanTicks = 35 * 365 * 24 * 60 # years * days * hours * mins
        self.maturityTicks = 5 * 365 * 24 * 60

        if isNewborn:
            self.ticksAlive = 0
        else:
            self.ticksAlive = random.randint(0, self.lifespanTicks - 1)

        if self.ticksAlive >= self.maturityTicks:
            if random.randint(0, 1) == 0:
                self.sex = "M"
            else:
                self.sex = "F"

            self.isMature = True
        else:
            self.sex = "X"
            self.isMature = False

        self.hunger = 10 # going to starve after 20
        self.survivalProbability = .95 # they can regenerate, after all
        self.movementImpact = .1

    def performStandardAction(self):
        if self.ticksAlive >= self.lifespanTicks:
            self.die('old age!') # die of old age

        if self.isMature == False and self.ticksAlive >= self.maturityTicks:
            self.isMature = True
            if random.randint(0, 1) == 0:
                self.sex = "M"
            else:
                self.sex = "F"

        if self.isMature == False and self.hunger <= 2: # some starfish reproduce asexually when food is plentiful
            self.reproduce()
        else:
            myBlock = self.ecosystem.getSeaBlock(self.location)
            neighborOrgs = myBlock.getOrganisms()
            for org in neighborOrgs:
                if self.hunger > 0 and self.ecosystem.isEdible(self, org):
                    org.beEaten()
                    self.hunger -= 1
                    break
                elif type(org) == type(self): # found a fellow shark!
                    if self.isMature and org.isMature and self.sex == "F" and org.sex == "M":
                        self.reproduce()
                        break
        if self.hunger > 20:
            self.die('starvation!')
        self.hunger += 1 # every tick get 1 more hunger unit
        self.randomDirection()
        self.move()
        self.ticksAlive += 1

    def reproduce(self):
        baby = Starfish(self.ecosystem, self.location, True)
        self.ecosystem.addNewborn(baby)

    def printStatus(self):
        return
                


