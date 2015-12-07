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
shrimpColor = (236, 69, 240)
tunaColor = (255, 251, 10)
sharkColor = (235, 23, 17)
manateeColor = (103, 242, 232)
seastarColor = (238,128,21)
grouperColor = (196,188,169)
herringColor = (138, 215, 110)

def graphicsOutput(orgsList, filename, rows, cols):
    vdim = 51*rows
    hdim = 51*cols
    picture = Image.new("RGB", (hdim, vdim))
    pix_map = picture.load()
    for i in range(hdim):
        if i%51 == 0 and i != 0:
            for j in range(vdim): pix_map[i,j] = (255, 255, 255)
        for j in range(vdim):
            if j % 51 == 0 and j != 0: pix_map[i,j] = (255, 255, 255)
    for org in orgsList:
        if type(org) == Coccolithophores:
            loc = org.location
            cornerH, cornerV, width, height=graphics_location_block(loc)
            for i in range(cornerH, (cornerH+height)):
                for j in range(cornerV, (cornerV+width)):
                    printpixel = random.uniform(0,1)
                    if printpixel > 0.9:
                        r, g, b = pix_map[i,j]
                        g = g+((255-g)*((2000000)/(255-g+1)))
                        pix_map[i,j] = (r, g, b)
        if type(org) == Shrimp:
            loc = org.location
            x, y = graphics_location(loc)
            
            squaresize=1
            if org.population > 40: squaresize=3
            if org.population > 120: squaresize=5
            if org.population > 180: squaresize=7
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



def graphics_location_block(loc):
    return (int(loc.row)*51, int(loc.col)*51, 50, 50)

def graphics_location(loc):
    return (int(loc.row*51), int(loc.col*51))

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


def printCircle(x, y, size, hdim, vdim):
    pixels = []
    semicircle = int(size/2)
    decline = 1
    colLength = 0
    for i in range(x-semicircle, x+semicircle+1):
        if i < 0: continue
        if i >= hdim: break
        for j in range(y-colLength, y+colLength+1):
            pixels.append((i,j))
    colLength += decline
    if colLength == semicircle: decline = -1
    return pixels



def write_picture(picture, filename, hdim, vdim):
    csv=open(filename, "w")
    for i in range(hdim):
        for j in range(vdim):
            r, g, b=picture[i,j]
            csv.write("" +str(r) +" " +str(g) +" " +str(b) +",")
        csv.write("\n")
