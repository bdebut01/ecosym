# LET IT BE KNOWN THIS IS A TESTING CLASS, NOT AN ACTUAL ORGANISM
import ecosystem
import seablock
import location
from organism import Organism
class Bulbasaur(Organism):
	def __init__(self, ecosystem, location = None):
		Organism.__init__(self, ecosystem, location)
	
	def printStatus(self):
		print "Doin bulba-things, you know at location: " + "(" + str(self.location.row) + ", " + str(self.location.col) + ")"