#graphic_output module
#handles printing of graphics from the ecosystem
#Part of the EcoSym Project
#Mostly written by Nathan Stocking (contact for questions)
#with contributions from Reema Al-Marzoog and Ben DeButts
#employs the Pillow module. If an import error results, use
#sudo pip install Pillow

#import each organism type for printing
from coccolithophores import Coccolithophores
from shrimp import Shrimp
from tuna import Tuna
from shark import Shark
from manatee import Manatee
from starfish import Starfish
from grouper import Grouper
from herring import Herring
from PIL import Image
from location import Location
import random

#colors for each organism are specified here.
#If an organism is not mentioned, it may have a more sophisticated mechanism.
#shapes are not specified, as more complex calculations are performed.
shrimpColor = (236, 69, 240)
tunaColor = (255, 251, 10)
sharkColor = (235, 23, 17)
manateeColor = (103, 242, 232)
seastarColor = (238,128,21)
grouperColor = (196,188,169)
herringColor = (138, 215, 110)

#call this function with a list of organisms, a width and height in blocks and a graphic will result

def graphicsOutput(orgsList, filename, rows, cols):
    #set up a blank image (all black)
    vdim = 51*rows
    hdim = 51*cols
    picture = Image.new("RGB", (hdim, vdim))
    pix_map = picture.load()
    #draw white line barriers between blocks
    for i in range(hdim):
        if i%51 == 0 and i != 0:
            for j in range(vdim): pix_map[i,j] = (255, 255, 255)
        for j in range(vdim):
            if j % 51 == 0 and j != 0: pix_map[i,j] = (255, 255, 255)
            #now handle printing of each organism in turn
    for org in orgsList:
        if type(org) == Coccolithophores:   #coccolithophores manifest as green dots
        #the greater the population, the greener they are
        
            loc = org.location
            cornerH, cornerV, width, height=graphics_location_block(loc)
            for i in range(cornerH, (cornerH+height)):
                for j in range(cornerV, (cornerV+width)):
                    printpixel = random.uniform(0,1)
                    if printpixel > 0.9:
                        r, g, b = pix_map[i,j]
                        g = g+((255-g)*((2000000)/(255-g+1)))
                        pix_map[i,j] = (r, g, b)
                        #most other organisms print either as squares/rectangles
                        #or by pre-defined shapes
        if type(org) == Shrimp:
            loc = org.location
            x, y = graphics_location(loc)
            #the greater the population, the bigger the square
            squaresize=1
            if org.population > 20: squaresize=2
            if org.population > 50: squaresize=3
            if org.population > 80: squaresize=4
            if org.population > 120: squaresize=5
            if org.population > 160: squaresize=6
            if org.population > 200: squaresize=7
            for i in range(x-squaresize, x+squaresize+1):
                if i < 0: continue
                if i >= vdim: continue
                for j in range(y-squaresize, y+squaresize+1):
                    if j < 0: continue
                    if j >= hdim: break
                    pix_map[i,j] = shrimpColor
        if type(org) == Tuna:
            loc = org.location
            x, y = graphics_location(loc)
            for i in range(x-2, x+3):
                if i < 0: continue
                if i >= vdim: break
                for j in range(y-4, y+5):
                    if j < 0: continue
                    if j >= hdim: break
                    pix_map[i,j] = tunaColor
        if type(org) == Shark:
            loc = org.location
            x, y = graphics_location(loc)
            pixels = printFishShape(x, y, hdim, vdim)
            for i in pixels:
                pix_map[i] = sharkColor
        if type(org) == Manatee:
            loc = org.location
            x, y = graphics_location(loc)
            for i in range(x-4, x+5):
                if i < 0: continue
                if i >= vdim: break
                for j in range(y-4, y+5):
                    if j < 0: continue
                    if j >= hdim: break
                    pix_map[i,j] = manateeColor
        if type(org) == Starfish:
            loc = org.location
            x, y = graphics_location(loc)
            for i in range(x-2, x+3):
                if i < 0: continue
                if i >= vdim: break
                for j in range(y-2, y+3):
                    if j < 0: continue
                    if j >= hdim: break
                    pix_map[i,j] = seastarColor
        if type(org) == Grouper:
            loc = org.location
            x, y = graphics_location(loc)
            for i in range(x-4, x+5):
                if i < 0: continue
                if i >= vdim: break
                for j in range(y-2, y+3):
                    if j < 0: continue
                    if j >= hdim: break
                    pix_map[i,j] = grouperColor
        if type(org) == Herring:
            loc = org.location
            x, y = graphics_location(loc)
            for i in range(x-1, x+2):
                if i < 0: continue
                if i >= vdim: break
                for j in range(y-4, y+5):
                    if j < 0: continue
                    if j >= hdim: break
                    pix_map[i,j] = herringColor
    picture.save(filename)
    #picture.show()
    #write_picture(pix_map, "test.csv", hdim, vdim)


#return the pixel coordinates of the block in which the given location can be found
#used to print something globally to the block
#example: the coccolithophores print dots over the entire block, not just in one area
def graphics_location_block(loc):
    return (int(loc.row)*51, int(loc.col)*51, 50, 50)

#return the pixel best located for the given location
#used to print an organism with more
#specific location data
#used in this simulation for all mobile organisms
def graphics_location(loc):
    return (int(loc.row*51), int(loc.col*51))

#function to print a vaguely fish-like shape
#used for shark because there are only so many rectangles
def printFishShape(x, y, hdim, vdim):
    pixels = []
    colLengths = [1, 1, 1, 2, 2, 3, 3, 2, 2, 1, 1, 0, 0]
    #start 7 columns back, 3 for the tail
    for i in range(x-7, x+6):
        if i < 0: continue
        if i >= hdim: break
        for j in range(y-colLengths[(i+7-x)], y+colLengths[(i+7-x)]+1):
            if j < 0: continue
            if j >= hdim: break
            pixels.append((i,j))
    return pixels


#a debug function
#takes a pixel map and dumps data to a csv file, which can be opened as a spreadsheet
#this is not intended to be run
#it was included because one of the original writers is blind
#and used it as a testing module
def write_picture(picture, filename, hdim, vdim):
    csv=open(filename, "w")
    for i in range(hdim):
        for j in range(vdim):
            r, g, b=picture[i,j]
            csv.write("" +str(r) +" " +str(g) +" " +str(b) +",")
        csv.write("\n")
