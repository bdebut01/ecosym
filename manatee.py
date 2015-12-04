# Primary predator of coccolithophores, tho in real life, they eat plants not plankton
import random
from organism import Organism

class Manatee(Organism):
	def __init__(self, ecosystem, location = None, isNewborn = False):
		Organism.__init__(self, ecosystem, location)
		if random.randint(0, 1) == 0:
			self.sex = "M"
		else:
			self.sex = "F"

		if isNewborn:
			self.ticksAlive = 0
		else: # Give insantiated manatee random age
			self.ticksAlive = random.randint(0, 60)
		# Who knew? Manatees can live up to 60 years old
		self.lifespanTicks = 60 * 365 * 24 * 60 # years * days * hours * mins
		self.survivalProbability = 0.2 # don't think they are the best survivors
		self.movementImpact = .1
		self.hunger = 50

	def performStandardAction(self):
		if self.ticksAlive >= self.lifespanTicks:
			self.die('old age!') # die of old age
		prey = None
		myBlock = self.ecosystem.getSeaBlock(self.location)
		neighborOrgs = myBlock.getOrganisms()
		for org in neighborOrgs:
			if type(org) == type(self): # found a fellow manatee!
				if org.sex != self.sex:
					self.reproduce()
					break
			elif self.ecosystem.isEdible(self, org):
				prey = org
				break
		if prey != None:
			food = prey.beEaten()
			self.hunger -= (food/15000)
		
		self.hunger += 1 # every tick get 1 more hunger unit

		if self.hunger > 100: # starve, (like normal animals, not like threads)
			self.die('starvation!')
		self.randomDirection()
		self.move()
		self.ticksAlive += 1

	def reproduce(self):
		babyMan = Manatee(self.ecosystem, self.location)
		self.ecosystem.addNewborn(babyMan)

	def printStatus(self):
		#print "Manatee here"
		return
