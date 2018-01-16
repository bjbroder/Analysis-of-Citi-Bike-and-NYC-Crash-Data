#!/usr/bin/env python3

#taken from wikipedia "Even-odd rule" @ https://en.wikipedia.org/wiki/Even%E2%80%93odd_rule

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
           (x < poly[i][0] + (poly[j][0] - poly[i][0]) * (y - poly[i][1]) /
            (poly[j][1] - poly[i][1])):
            c = not c
        j = i
    return c

manhatPoly = [               #polygon that approximates the shape of manhattan
    (-74.012344,40.705452),
    (-74.005992,40.751633),
    (-73.926856,40.87363),
    (-73.912094,40.872332),
    (-73.936126,40.836496),
    (-73.932693,40.797782),
    (-73.976982,40.736677),
    (-73.980071,40.71326)
    ]

import sys

fin = "bikeEndpoints" + sys.argv[1]
fout = "bikeBlobs" + sys.argv[1]

endPoints = open(fin)
bikeBlobs = open(fout,"w")

line = endPoints.readline()

while (line):
    route = line.split(",") #split each line on ,

    xStart = float(route[1]) #starting long
    yStart = float(route[0]) #starting lat

    xEnd = float(route[3]) #ending long
    yEnd = float(route[2]) #ending lat

    #checks if start and end coordinate of bike route are in the manhattan approximation
    if isPointInPath(xStart, yStart, manhatPoly) and isPointInPath(xEnd, yEnd, manhatPoly):

        #turns the bike route line into a parallelogram within which the bike is presumed to have travelled
        #parallelogram (here called a "bike Blob") is created by starting the upper left corner from .005 degrees latitude
        #above the starting lat and the bottom left corner .005 degrees latitude below the starting lat (same is done with ending lat)
        leftUpper = yStart + .005
        leftLower = yStart - .005
        rightUpper = yEnd + .005
        rightLower = yEnd - .005

        #print vertices of the bike blob, separate by commas, to the file that bikeBlobs equals (either "bikeBlobsJan" or "bikeBlobsYear")
        print (xStart, leftLower, leftUpper, xEnd, rightLower, rightUpper, route[4], route[5], route[6], sep = ",", end="", file=bikeBlobs)

    line = endPoints.readline()

endPoints.close()
bikeBlobs.close()

