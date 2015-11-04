class SeaBlock :
	def __init__(self, salinity = 1, sun = 0, oxygen = 0, pressure = 0) :
		self.__salinity  = sal
		self.__sunlight  = sun
		self.__oxygen  	 = oxy
		self.__pressure  = press
		self.__organisms = {}

	def removeOrganism(id) :
		del self.__organisms[id]

	def addOrganism(id, Creature) :
		self.__organisms[id] = Creature

	def setSunlight(val) :
		self.__sunlight = val
