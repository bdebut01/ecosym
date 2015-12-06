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
        if predator in self.__foodchain:
            self.__foodchain[predator].append(prey)
        else:
            self.__foodchain[predator] = [prey]

    # same thing as addRelationship but associates multiple prey with a predator
    # instead of just one type of prey
    def addMultiRelationship(self, predator, listOfPrey):
        for prey in listOfPrey:
            self.addRelationship(predator, prey)

    # tells you if the predator can eat the potential prey (note: pass in a type of
    # an instance of an organism subclass. 
    # e.g. isEdible(shark.Shark, fish.Fish) should return True
    def isEdible(self, pred, prey):
        if pred in self.__foodchain and prey in self.__foodchain[pred]:
            return True
        else:
            return False

