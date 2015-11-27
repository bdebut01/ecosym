# creates a dictionary where the keys and vals are organism subclass
# types. The keys represent the "predators" and the
# vals are lists of the "prey" they can eat. e.g. it could tell you that
# a shark can eat a fish. that would look something like this:
# { <type 'shark.Shark'>: [<type 'fish.Fish'>] }
class Foodchain():
    def __init__(self):
        self.__foodchain = {}

    # predator and prey arguments must be the type of an organism, i.e. 
    # <type 'shark.Shark'> (the way to call this, for example, is
    # addRelationship(shark.Shark, fish.Fish)
    def addRelationship(self, predator, prey):
        if predTy in self.__foodchain:
            self.__foodchain[predTy].append(preyTy)
        else:
            self.__foodchain[predTy] = [preyTy]

    # same thing as addRelationship but associates multiple prey with a predator
    # instead of just one type of prey
    def addMultiRelationship(self, predator, listOfPrey):
        for prey in listOfPrey:
            addRelationship(predator, prey)

    # tells you if the predator can eat the potential prey (note: pass in an
    # an instance of an organism subclass. 
    # e.g. myShark = Shark(...)
    #      myFish = Fish(...)
    #      isEdible(myShark, myFish) # should return True
    def isEdible(self, predator, prey):
        predTy = type(predator)
        preyTy = type(prey)
        if predTy in self.__foodchain and preyTy in self.__foodchain[predTy]:
            return True
        else:
            return False

