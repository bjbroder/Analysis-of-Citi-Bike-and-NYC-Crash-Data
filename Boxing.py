#!/usr/bin/env python3
from datetime import time
import sys

#takes a string of hours and minutes and converts them to time objects
def fixTime(someTime):
    splitTime = someTime.split(":")

    #if the first "digit" of the hours (or minutes) is 0, save only the second digit
    fixedTime  = [x[1] if (x[0] == "0" and len(x) > 1) else x for x in splitTime]
    return time(int(fixedTime[0]),int(fixedTime[1]))

#check if a bike blob's endpoint intersect with either a crash or box depening on the input param
def intersect(ep,x,y,itype,boxWidth=0):
    if itype == "box":
        xLeft = x
        xRight = x + boxWidth
        yBot = y
        yTop = y + boxWidth
    else: #type = "crash"
        xLeft = x
        xRight = x
        yBot = y
        yTop = y
    #can only intersect if the rightmost point x of the box/crash is farther right than the left side of the bike blob
    #and the leftmost point x of the box/crash (in crash, left and right x are the same) is farther left from the right side of the bike blob

    #if trying to see if a bike blob is in a box, immediately know its
    #true if all four corners of the blob are within the box (ie enclosed)
    if ep[0] < xRight and ep[3] > xLeft: 
        if itype != "crash" and \
           ((ep[1] < yTop and ep[1] > yBot) or \
            (ep[2] < yTop and ep[2] > yBot)) and \
           ((ep[4] < yTop and ep[4] > yBot) or \
            (ep[5] < yTop and ep[5] > yBot)):
            return True
        else:  #either checking "crash" or if blob intersects but is not enclosed by box
            yChange = ep[2]-ep[5]
            xChange = ep[0]-ep[3]
            if xChange != 0:
                m = yChange/xChange
                bTop = ep[2] - m*ep[0]
                bBot = ep[1] - m*ep[0]
                topCheck = m*xLeft + bTop #y = mx + b
                botCheck = m*xLeft + bBot
            else:
                topCheck = ep[2]
                botCheck = ep[1]
            if topCheck > yBot and botCheck < yTop: #if bottom y of box/crash is less than top of blob and top y is greater than bottom of blob, intersects
                return True
        return False

#reads in either "bikeBlobsJan" and "manhatCrashJan" or
#"bikeBlobsYear" and "manhatCrashYear" depending on input
def readFiles():
    finB = "bikeBlobs" + sys.argv[1]
    b = open(finB)
    bikes = b.readlines()
    b.close()

    finC = "manhatCrash" + sys.argv[1]
    c = open(finC)
    crashes = c.readlines()
    c.close()
    
    return bikes, crashes

#reads in the lon,lat pairs from box coords and saves them as dictionary keys
def dictBoxes():
    b = open("boxCoords")
    line = b.readline()
    boxes = {}
    while line:
        key = line[:len(line)-1] #gets rid of the newline character
        boxes[key] = [[],0,[],0] #value is a list of an empty list, 0 ,empty list, 0
        line = b.readline()
    return boxes

def listCrashes(crashes):
    noBikeAtCrash = [] #list that will first hold all crashes and later have some removed to only hold those crashes that were not near any bikes at the time of crash
    newCrashes = [[0]*3 for i in range (len(crashes))] #list where each element is a list of crash location, date, and time
    for c in range(len(crashes)):
        crash = crashes[c].split(",")
        x = float(crash[0]) #lon
        y = float(crash[1]) #lat
        cLoc = (x,y)
        cDate = crash[2]
        cTime = fixTime(crash[3]) #change to time object
        cVal = [cLoc,cDate,cTime]
        newCrashes[c] = cVal
        
        noBikeAtCrash.append(newCrashes[c])

    return newCrashes, noBikeAtCrash #new crashes is just called "crashes" when returned

def countCrashesBikes(boxes,bikes,crashes,noBikeAtCrash,boxWidth):
    nBAC = noBikeAtCrash
    
    crashInRoute = {}

    #turn each bike route into a key where the value is a list of crashes that were near the bike blob
    for b in bikes:
        bike = b.split(",")
        bikePoints = [float(bike[i]) for i in range (6)] #route coords are float-ified
        bDate = bike[6]
        bStart = fixTime(bike[7]) #change to time object
        bEnd = fixTime(bike[8]) #change to time object

        cInR = [] #stands for "crashes in route"

        #for each crash, check if that crash intersects the bike blob happened in the same time frame
        for c in crashes:
            x = c[0][0]
            y = c[0][1]
            cDate = c[1]
            cTime = c[2]

            #checks if the crash a bike ride dates are the same and if the crash happened while the route was "active"
            if cDate == bDate and cTime > bStart and cTime < bEnd \
                and intersect(bikePoints,x,y,"crash"): #check if the crash intersects with the bike blob
                cInR.append(c) #if so, add to list keeping track of crashes in route
                if c in nBAC: #if this crash is still in the list of "no bikes at crash", remove it
                    nBAC.remove(c)
        crashInRoute[str(bikePoints)] = cInR #after checking all of the crashes, all of the crashes intersecting the bike route are set as the value (list) where the route is the key
    return crashInRoute, nBAC

def addCrashesToBox(lon,lat,crashList,boxes,slot,boxWidth):
    box = str(lon) + "," + str(lat) #make the box's key out of long and lat
    crashesInBox = 0
    for crash in crashList:
        x = crash[0][0]
        y = crash[0][1]

        #if the crash's x is between the boxes sides
        #and the chrash's y is between the boxes top and bottom
        #and the crash was not already appended (this prevents getting duplicates)
        if x > lon and x < lon+boxWidth \
           and y > lat and y  < lat+boxWidth \
           and crash not in boxes[box][slot]: 
               boxes[box][slot].append(crash) #append the crash to the slot passed in (0 = near at least 1 bike; 2 = not near any bike)
               crashesInBox += 1 #keep track of num crashes appended
    return crashesInBox
                    
def fillBoxes(crashInRoute,boxes,boxWidth,noBikeAtCrash):
    for key in crashInRoute: #key is a bike route
        k = key.split(",")
        k[0] = k[0][1:]
        k[-1] = k[-1][:-1]
        route = [float(k[i]) for i in range (len(k))] #float-ifying route coords

        #for each bike route, check each box to see if there is an intersection
        for box in boxes: 
            coords = box.split(",")
            lon = float(coords[0])
            lat = float(coords[1])

            #if there is an intersection, check all of the crashes that intersected with the bike blob to see if they also intersect the box
            if intersect(route,lon,lat,"box",boxWidth): 
                if len (crashInRoute[key]) != 0: #if there are crashes that happened in the bike blob
                    crashesInBox = addCrashesToBox(lon,lat,crashInRoute[key],boxes,0,boxWidth) #see if the crashes are also in the box and
                                                        #if so append them to spot 0 int the box's value list
                        #keep track of num crashes appended
                    if crashesInBox != 0:   #because if so, that means that this bike was near at least one car crash specifically in this box
                        boxes[box][1] += 1  #therefore, this bike route gets counted towards bikes near crashes in this box (slot 1)
                    else:                   #this bike was not near any crashes in this box (crashes in blob fell into other boxes)
                        boxes[box][3] += 1  #therefore, this bike route gets counted towards bikes not near crashes in this box (slot 3)
                else:
                    boxes[box][3] += 1      #no crashes were near the bike so it gets counted towards bikes not near crashes in this box

    for box in boxes: #need to look through boxes again and now look through each car crash that was not near any bike route to see if it was in the box
        coords = box.split(",")
        lon = float(coords[0])
        lat = float(coords[1])

        crashesInBox = addCrashesToBox(lon,lat,noBikeAtCrash,boxes,2,boxWidth) #if its in the box, gets appended to slot 2 which has crashes not near any bikes

    return boxes

def writeOut(boxes):
    fout = "filledBoxes" + sys.argv[1] #write out to either "filledBoxesJan" or "filledBoxesYear" depending on input
    f = open(fout,"w")
    
    for box in boxes:
        b = box.split(",")
        #prints to file the box coords (lat, lon), the num of crashes near bikes, the num of bikes near crashes, \
        #the num of crashes not near any bikes, the num of bikes not near any crashes
        print(b[1] + "|" + b[0] + "|" + str(len(boxes[box][0])) + "|" + \
              str(boxes[box][1]) + "|" + str(len(boxes[box][2])) + "|" + \
              str(boxes[box][3]), file=f)
    f.close()

def main():    
    boxWidth = .005 #small arbitrary num for box width; bust be the same a width from "makeBoxes.py"
    boxShift = .001 #smaller arbitary number for box height; must be same as shift from "makeBoxes.py"
    bikes, crashes = readFiles()
    boxes = dictBoxes()
    crashes, noBikeAtCrash = listCrashes(crashes)
    crashInRoute, noBikeAtCrash = countCrashesBikes(boxes,bikes,crashes,noBikeAtCrash,boxWidth)
    filledBoxes = fillBoxes(crashInRoute,boxes,boxWidth,noBikeAtCrash)
    writeOut(filledBoxes)

main()
