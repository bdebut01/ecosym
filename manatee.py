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

	def performStandardAction(self):
		if self.ticksAlive >= self.lifespanTicks:
			self.die() # die of old age

		myBlock = self.ecosystem.getSeaBlock(self.location)
		neighborOrgs = myBlock.getOrganisms()
		for org in neighborOrgs:
			if type(org) == type(self): # found a fellow manatee!
				if org.sex != self.sex:
					self.reproduce()
					break
			elif self.ecosystem.isEdible(self, org):
				org.beEaten()
				break
		self.ticksAlive += 1

	def reproduce(self):
		babyMan = Manatee(self.ecosystem, self.location)
		self.ecosystem.addNewborn(babyMan)

	def printStatus(self):
		#print "Manatee here"
		return

