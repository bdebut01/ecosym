class SeaBlock :
	def __init__(self, salinity = 1, sun = 0, oxygen = 0, pressure = 0) :
		self.__salinity  = salinity
		self.__sunlight  = sun
		self.__oxygen  	 = oxygen
		self.__pressure  = pressure
		self.__organisms = {}

	def removeOrganism(self, id) :
		del self.__organisms[id]

	def addOrganism(self, id, Creature) :
		self.__organisms[id] = Creature

	def setSunlight(self, val) :
		self.__sunlight = val
