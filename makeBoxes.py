#!/usr/bin/env python3

def isPointInPath(x, y, poly):
      #      """
      #  x, y -- x and y coordinates of point
      #  poly -- a list of tuples [(x, y), (x, y), ...]
      #  """
    num = len(poly)
    i = 0
    j = num - 1
    c = False
    for i in range(num):
        if ((poly[i][1] > y) != (poly[j][1] > y)) and \
           (x < poly[i][0] + (poly[j][0] - poly[i][0]) * (y - poly[i][1]) \
            / (poly[j][1] - poly[i][1])):
            c = not c
        j = i
    return c

#approximation for the shape of manhattan
manhatPoly = [
    (-74.012344,40.705452),
    (-74.005992,40.751633),
    (-73.926856,40.87363),
    (-73.912094,40.872332),
    (-73.936126,40.836496),
    (-73.932693,40.797782),
    (-73.976982,40.736677),
    (-73.980071,40.71326)
]


#This generates lat and longs that shift over by .001 degrees in lat and long
#Together, lat and long pairs represent .005x.005 degree sq boxes that cover the city of manhattan

#arbitrary number that is use throughout the box-related files
boxWidth = .005 #very small number to be width/height of box
boxShift = .001 #even smaller number to be the shift to the right (and when that loop hits the end - up and restart at left) so that the boxes overlap

#starts by creating boxes from a broader boundry that surrounds manhattan
manhatCoords = [40.70, -74.025,40.87,-73.90]

lat = manhatCoords[0] #y
lon = manhatCoords[1] #x

fout =  "boxCoords"
f = open(fout,"w")

#while you are below the upper bound of the box
while lat < manhatCoords[2]:
    
    #while you are within the rightmost bound of the box
    while lon < manhatCoords [3]:

        #assuming if all four corners of the box are in manhttan that the box is fully in manhattan (ie assuming that none of the manhatPoly and box edges intersect)
        if isPointInPath(lon, lat, manhatPoly) and \
           isPointInPath(lon+boxWidth, lat, manhatPoly) and \
           isPointInPath(lon, lat+boxWidth, manhatPoly) and \
           isPointInPath(lon+boxWidth, lat+boxWidth, manhatPoly) :

            #"lon,lat" will become the key to a dictionary created in a future program
            print(str(lon) + "," + str(lat), file = f)

        #shifts the lon rightwards but prevents very long decimals to makie viewing the boxes in columns easier)    
        lon = round(lon+boxShift,3)

    #resets the lon at the left side of the manhattan boundry    
    lon = manhatCoords[1]
    #shifts the lat upwards
    lat = round(lat+boxShift,3)
