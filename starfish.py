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

        self.hunger = 50
        self.starvationLevel = 100
        self.survivalProbability = .95 # they can regenerate, after all
        self.movementImpact = .1 # slowly crawl along the ocean floor

    def performStandardAction(self):
        if self.ticksAlive >= self.lifespanTicks:
            self.die('old age!') # die of old age

        self.__updateMaturityLevel()

        if self.isMature == False and self.hunger <= 2: 
            # some immature starfish reproduce asexually when food is plentiful
            self.reproduce()
        else:
            self.__lookForPreyAndMates()

        self.__handleAndUpdateHunger()
        self.__chooseDirectionAndMove()
        self.ticksAlive += 1

    def __chooseDirectionAndMove(self):
        if self.ticksAlive % 3 == 0:
            # every few ticks, choose a random direction
            self.randomDirection()
        self.move()

    def __handleAndUpdateHunger(self):
        if self.hunger > self.starvationLevel:
            self.die('starvation!')
        self.hunger += 1 

    def __lookForPreyAndMates(self):
        neighborOrgs = self.ecosystem.getNeighbors(self)
        for org in neighborOrgs:
            if self.hunger > 0 and self.ecosystem.isEdible(self, org):
                food = org.beEaten()
                self.hunger -= (food / 15000)
                break
            elif type(org) == type(self): # found a fellow starfish!
                if self.isMature and org.isMature:
                    if self.sex == "F" and org.sex == "M":
                        self.reproduce()
                        break
    
    def __updateMaturityLevel(self):
        if self.isMature == False and self.ticksAlive >= self.maturityTicks:
            self.isMature = True
            if random.randint(0, 1) == 0:
                self.sex = "M"
            else:
                self.sex = "F"

    def reproduce(self):
        baby = Starfish(self.ecosystem, self.location, True)
        self.ecosystem.addNewborn(baby)

    def printStatus(self):
        return
                


