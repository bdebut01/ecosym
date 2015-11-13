from sets import Set

class SeaBlock :
	def __init__(self, salinity = 1, sun = 0, oxygen = 0, pressure = 0) :
		self.__salinity  = salinity
		self.__sunlight  = sun
		self.__oxygen  	 = oxygen
		self.__pressure  = pressure
		self.__organisms = Set()

	def removeOrganism(self, organism) :
		self.__organisms.remove(organism)

	def addOrganism(self, Creature) :
		self.__organisms.add(Creature)

	def setSunlight(self, val) :
		self.__sunlight = val
