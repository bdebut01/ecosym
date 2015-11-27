from sets import Set
from thread_functions import with_lock
from threading import Lock

class SeaBlock :
    def __init__(self, salinity = 1, sun = 0, oxygen = 0, pressure = 0) :
        self.__salinity  = salinity
        self.__sunlight  = sun
        self.__oxygen  	 = oxygen
        self.__pressure  = pressure
        self.__organisms = Set()
        self.__orgsLock = Lock()

    def removeOrganism(self, organism) :
        def remove():
            if organism in self.__organisms:
                self.__organisms.remove(organism)
        with_lock(self.__orgsLock, remove)

    def addOrganism(self, Creature) :
        with_lock(self.__orgsLock, lambda : self.__organisms.add(Creature))

    def setSunlight(self, val) :
        self.__sunlight = val

    def getSalinity(self): return self.__salinity
    def getSunlight(self): return self.__sunlight
    def getOxygen(self): return self.__oxygen
    def getPressure(self): return self.__pressure
    def getOrganisms(self): return self.__organisms

    def printAttributes(self):
        print "Salinity: " + str(self.getSalinity())
        print "Sunlight: " + str(self.getSunlight())
        print "Oxygen: " + str(self.getOxygen())
        print "Pressure: " + str(self.getPressure())


