#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt

f = "sortedPercents" + sys.argv[2] + sys.argv[1] #type of plot, data

fin = open(f)

line = fin.readline()

x = []
y = []
colors = []

pdf = plt.figure()

while (line):
    l = line.split("|")
    x.append(float(l[1])) #long
    y.append(float(l[0])) #lat

    p = 0
    q = 0
    
    if sys.argv[2] == "Bike" or sys.argv[2] == "TotBike": #if plotting percent bikes near crashes or total bikes
        if sys.argv[2] == "Bike": p = float(l[6]) #bike percent column
        else: q = float(l[8]) #total bike column

        #colors that change by percent creating heatmap effect
        if q > 3500:    colors.append("xkcd:blood")
        elif q > 3250:    colors.append("xkcd:burgundy") 
        elif p > 1.2 or q > 3000:    colors.append("xkcd:dark red")
        elif p > 1.1 or q > 2750:    colors.append("xkcd:brick red")
        elif p > 1.0 or q > 2500:    colors.append("xkcd:red")
        elif p > 0.9 or q > 2250:    colors.append("xkcd:dark orange")
        elif p > 0.8 or q > 2000:    colors.append("xkcd:pumpkin")
        elif p > 0.7 or q > 1750:    colors.append("xkcd:orange")
        elif p > 0.6 or q > 1500:    colors.append("xkcd:yellow orange")
        elif p > 0.5 or q > 1250:    colors.append("xkcd:dark yellow")
        elif p > 0.4 or q > 1000:    colors.append("xkcd:goldenrod")
        elif p > 0.3 or q > 750:    colors.append("xkcd:sun yellow")
        elif p > 0.2 or q > 500:    colors.append("xkcd:yellow")
        elif p > 0.1 or q > 250:    colors.append("xkcd:dark cream")
        elif p > 0 or q > 0:      colors.append("xkcd:green yellow")
        else: colors.append("xkcd:green")

    else: #if plotting percent crashes near bikes
        if sys.argv[2] == "Crash": p = float(l[7]) #crash percent column
        else: q = float(l[9]) #total crash column
        
        #colors that change by percent creating heatmap effect
        if   p == 100 or q > 50:    colors.append("xkcd:dark purple")
        elif p > 90 or q > 45:    colors.append("xkcd:plum")
        elif p > 80 or q > 40:    colors.append("xkcd:royal purple")
        elif p > 70 or q > 35:    colors.append("xkcd:grape")
        elif p > 60 or q > 30:    colors.append("xkcd:purple")
        elif p > 50 or q > 25:    colors.append("xkcd:purple blue")
        elif p > 40 or q > 20:    colors.append("xkcd:cornflower")
        elif p > 30 or q > 15:    colors.append("xkcd:carolina blue")
        elif p > 20 or q > 10:    colors.append("xkcd:lightblue")
        elif p > 10 or q > 5:    colors.append("xkcd:light blue")
        elif p > 0 or q > 0:    colors.append("xkcd:robin's egg")
        else: colors.append("xkcd:ice blue")

    line = fin.readline()

#creates scatter plot based on lon/lat made of squares (representing
#the manhattan boxes although not size accurate) the are semi-transparent
plt.scatter(x,y, c = colors, s = 100, marker = 's', alpha = .1)

plt.xlabel("Longitude")
plt.ylabel("Latitude")

fout = "manhattan" + sys.argv[2] + sys.argv[1] + ".pdf"

pdf.savefig(fout)
