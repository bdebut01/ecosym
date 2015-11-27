import sys
from ecosystem import Ecosystem
import ecosystem
from seablock import SeaBlock
from location import Location

# Import global variables for entire simulation, (e,g: creature dictionary)
#import variables 
# ^ this wasn't working so i just pasted the variables into my inputCreatures func
global creatures
global num_and_what_creatures
global creature_funcs

# ADD YOUR ORGANISM HERE, for recognition purposes
def presetCreatures():
	global creatures
	creatures = dict()
	global num_and_what_creatures
	num_and_what_creatures = dict() # key is creature_id, value is quantity
	# List off creature pairings
	creatures[0] = "Coccolithophores"
	creature_funcs[0] = coccolithophores.Coccolithophores # Halp
	creatures[1] = "Quadralopsaurus"
	creatures[2] = "Bulbasaur"
	creature_funcs[2] = bulbasaur.Bulbasaur
	creatures[3] = "These are test creatures"

def inputLoop():
	while True:
		user_input = raw_input()
		if user_input == 'q':
			break
		if len(user_input.split(' ')) != 2: # Ignore inputs with anything but 2 values
			continue
		else:
			key, value = user_input.split(' ')
	        if int(key) not in creatures:
	        	print "That key not found, ignoring"
	        else:
	        	# [0] is key, [1] is quantity
	        	if int(key) in num_and_what_creatures: #already added so we're going to just increment
	        		res = num_and_what_creatures[int(key)]
	        		value += res
	        	# Add the key and the value (whether it was affected or not by if statement)
	        	num_and_what_creatures[int(key)] = value
	        	print str(value) + " " + creatures[int(key)] + "s added"

def inputCreatures():
	# Load data structures with preset data
	presetCreatures()
	# Redeclare because we are modifying them in this function
	global creatures
	global num_and_what_creatures
	# Rattle off the dictionary of known creature to name pairings
	print "Known creatures:"
	for c in creatures:
		print (str(c) + ": " + creatures[c])
	print ''
	print "Input desired creatures ids & quantity separated by newline, enter \'q' to stop input"
	print "Example input for 10 coccolithophores: "
	print "0 10"
	print ''
	inputLoop()

# Everything works if you just comment out creature stuff
def main(argv):
	inputCreatures()
	ecosystem = Ecosystem(10, 10)
	loc = Location(3,4)
	ecosystem.loadCreatures(num_and_what_creatures, creature_funcs)

	block = ecosystem.getSeaBlock(loc)
	block.printAttributes()
    # ecosystem.startSimulation()

if __name__ == '__main__':
    main(sys.argv)

