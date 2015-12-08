import random
from organism import Organism

class Fish(Organism):
    def __init__(self, ecosystem, lifespanYears, maturityYears, location = None,
            isNewborn = False):
        Organism.__init__(self, ecosystem, location)

        self.lifespanTicks = lifespanYears * 365 * 24 * 60 # years * days * hours * mins
        self.maturityTicks = maturityYears * 365 * 24 * 60
        self.hunger = 10
        self.starvationLevel = 20

        self.__initializeSex()
        self.__initializeAgeAndMaturity(isNewborn)

    def performStandardAction(self):
        if self.ticksAlive >= self.lifespanTicks:
            self.die('old age!') # die of old age

        self.__updateMaturityLevel()
        self.__lookForPreyAndMates()
        self.__handleAndUpdateHunger()
        self.__chooseDirectionAndMove()
        self.ticksAlive += 1

    def printStatus(self):
        return

    def __initializeSex(self):
        if random.randint(0, 1) == 0:
            self.sex = "M"
        else:
            self.sex = "F"

    def __initializeAgeAndMaturity(self, isNewborn):
        if isNewborn:
            self.ticksAlive = 0
        else:
            self.ticksAlive = random.randint(0, self.lifespanTicks - 1)

        self.isMature = self.ticksAlive >= self.maturityTicks

    def __updateMaturityLevel(self):
        if self.isMature == False and self.ticksAlive >= self.maturityTicks:
            self.isMature = True

    def __lookForPreyAndMates(self):
        neighborOrgs = self.ecosystem.getNeighbors(self)
        for org in neighborOrgs:
            if type(org) == type(self): # found a fellow fish!
                if self.isMature and org.isMature:
                    if self.sex == "F" and org.sex == "M":
                        self.reproduce()
                        break
            elif self.hunger > 0 and self.ecosystem.isEdible(self, org):
                ate = org.beEaten()
                if ate: # if the prey didn't manage to get away
                    self.hunger -= 1
                    break

    def __handleAndUpdateHunger(self):
        if self.hunger > self.starvationLevel:
            self.die('starvation!')

        self.hunger += 1 # every tick get 1 more hunger unit

    def __chooseDirectionAndMove(self):
        self.randomDirection()
        self.move()



                


