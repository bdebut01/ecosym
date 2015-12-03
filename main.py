import sys
from ecosystem import Ecosystem
from coccolithophores import Coccolithophores
from bulbasaur 		  import Bulbasaur
from shark import Shark
from manatee import Manatee
from tuna import Tuna
from shrimp import Shrimp
from seablock import SeaBlock
from location import Location
import coccolithophores

# Import global variables for entire simulation, (e,g: creature dictionary)
#import variables 
# ^ this wasn't working so i just pasted the variables into my inputCreatures func
global creatures
global num_and_what_creatures
global creature_funcs

# ADD YOUR ORGANISM HERE, for recognition purposes
# Look at bulbasaur for example, but it does mean don't repeat organism IDs
def presetCreatures():
	global creatures
	global creature_funcs
	creatures = dict()
	global num_and_what_creatures
	num_and_what_creatures = dict() # key is creature_id, value is quantity
	global creature_funcs
	creature_funcs = dict()


	# List off creature pairings, add your organism HERE
	creatures[0] = "Coccolithophores"
	creature_funcs[0] = Coccolithophores # Halp
	# creatures[1] = "Bulbasaur"
	# creature_funcs[1] = Bulbasaur
	creatures[1] = "Shrimp"
	creature_funcs[1] = Shrimp
	creatures[2] = "Shark"
	creature_funcs[2] = Shark
	creatures[3] = "Tuna"
	creature_funcs[3] = Tuna
	creatures[2] = "Shark"
	creature_funcs[2] = Shark
	creatures[3] = "Tuna"
	creature_funcs[3] = Tuna
	creatures[4] = "Manatee"
	creature_funcs[4] = Manatee

def userDeclareOceanSize():
	print "--Input Ocean size--"
	print "--------------------"
	print "Example input: '10 10'"
	while True:
		user_input = raw_input()
		if len(user_input.split(' ')) != 2: # Ignore inputs with anything but 2 values
			print "Please input a valid ocean size, minimum 1 x 1, maximum block^2 is 900"
			continue
		else:
			width, height = user_input.split(' ')
			print "Height: " + str(height) + " Width: " + str(width)
			if not width.isdigit() or not height.isdigit() or int(width) < 1 or int(height) < 1 or int(width) * int(height) > 900:
				print "Minimum height and width is 1, max block^2 is 900, try again"
			else:
				print "OK, ocean width: " + str(width) + " ocean height: " + str(height)
				print '\n' 
				return (int(width), int(height))
			continue

# Can ignore me, I loop in stdin/stdout receiving organism IDs and quantities
#	Stop when 'q' is read in
def inputLoop(w, h):
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
                        value = int(value)
	        	if int(key) in num_and_what_creatures: #already added so we're going to just increment
	        		res = int(num_and_what_creatures[int(key)])
	        		value += res
	        	# Add the key and the value (whether it was affected or not by if statement)
	        	num_and_what_creatures[int(key)] = value
	        	print str(value) + " " + creatures[int(key)] + "s added"
	return (w, h)	        	

def inputCreatures():
	# Have user input ocean size
	width, height = userDeclareOceanSize()
	# Load data structures with preset data
	print "---Input Creatures---"
	print "---------------------"
	print '\n'
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
	return inputLoop(width, height)

# Everything works if you just comment out creature stuff
def main(argv):
	width, height = inputCreatures()
	ecosystem = Ecosystem(width, height)
	loc = Location(3,4)
	ecosystem.loadCreatures(num_and_what_creatures, creature_funcs)

	block = ecosystem.getSeaBlock(loc)
	block.printAttributes()
	ecosystem.startSimulation()

if __name__ == '__main__':
    main(sys.argv)

