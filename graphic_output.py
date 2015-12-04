from coccolithophores import Coccolithophores
from shrimp import Shrimp
from tuna import Tuna
from shark import Shark
from PIL import Image
from location import Location
import random

def graphicsOutput(orgsList, filename):
    picture = Image.new("RGB", (510, 510))
    pix_map = picture.load()
    for i in range(510):
        if i%51 == 0 and i != 0:
            for j in range(510): pix_map[i,j] = (255, 255, 255)
        for j in range(510):
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
    picture.save(filename)
    picture.show()
    write_picture(pix_map, "test.csv")



def graphics_location_block(loc):
    print(str(loc.row), str(loc.col))
    print(str(int(loc.row)*51) +str(int(loc.col)*51))
    return (int(loc.row)*51, int(loc.col)*51, 50, 50)

def graphics_location(loc):
    return {int(loc.row*51), int(loc.col*51), 50, 50}

def write_picture(picture, filename):
    csv=open(filename, "w")
    for i in range(510):
        for j in range(510):
            r, g, b=picture[i,j]
            csv.write("" +str(r) +" " +str(g) +" " +str(b) +",")
        csv.write("\n")