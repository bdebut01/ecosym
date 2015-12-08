
class Foodchain():
    """Foodchain class can be used to represent predator-prey relationships.
       
       Doesn't expect input of any particular type, but it should be consistent.
    """
    def __init__(self):
        self.__foodchain = {}

    def addRelationship(self, predator, prey):
        """Adds a predator-prey relationship to the foodchain."""
        if predator in self.__foodchain:
            self.__foodchain[predator].append(prey)
        else:
            self.__foodchain[predator] = [prey]

    def addMultiRelationship(self, predator, listOfPrey):
        """Associates all prey in listOfPrey (an array) with the predator."""
        for prey in listOfPrey:
            self.addRelationship(predator, prey)

    def isEdible(self, pred, prey):
        """ Returns True if the pred is a predator of prey, False otherwise."""
        if pred in self.__foodchain and prey in self.__foodchain[pred]:
            return True
        else:
            return False

