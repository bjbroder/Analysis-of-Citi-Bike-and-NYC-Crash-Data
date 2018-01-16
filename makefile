all:	manhattanBikeJan.pdf manhattanCrashJan.pdf manhattanTotBikeJan.pdf manhattanTotCrashJan.pdf \
	sortedPercentsBikeJan sortedPercentsCrashJan sortedPercentsTotBikeJan sortedPercentsTotCrashJan\
	percentsPerBoxJan filledBoxesJan boxCoords bikeBlobsJan bikeEndpointsJan manhatCrashJan

#plot of percent bikes near crashes in boxes of manhattan
manhattanBikeJan.pdf:	sortedPercentsBikeJan
	./plotBoxes.py Jan Bike

#plot of percent crashes near bikes in boxes of manhattan
manhattanCrashJan.pdf:	sortedPercentsCrashJan
	./plotBoxes.py Jan Crash

#plot of total bikes in manhattan
manhattanTotBikeJan.pdf:	sortedPercentsTotBikeJan
	./plotBoxes.py Jan TotBike

#plot of total crashes in manhattan
manhattanTotCrashJan.pdf:	sortedPercentsTotCrashJan
	./plotBoxes.py Jan TotCrash

#sorted prev by percent crashes near bikes so boxes with lower percentages get plotted first
sortedPercentsBikeJan:	percentsPerBoxJan
	cat percentsPerBoxJan | sort -t "|" -k 7 -n > sortedPercentsBikeJan

#sorted prev by percent bikes near crashes so boxes with lower percentages get plotted first
sortedPercentsCrashJan:	percentsPerBoxJan
	cat percentsPerBoxJan | sort -t "|" -k 8 -n > sortedPercentsCrashJan

#sorted prev by total bikes so boxes with fewer bikes get plotted first
sortedPercentsTotBikeJan:	percentsPerBoxJan
	cat percentsPerBoxJan | sort -t "|" -k 9 -n > sortedPercentsTotBikeJan

#sorted prev by total crashes so boxes with fewer crashes get plotted first
sortedPercentsTotCrashJan:	percentsPerBoxJan
	cat percentsPerBoxJan | sort -t "|" -k 10 -n > sortedPercentsTotCrashJan

#all prev + percent bikes near (of total bikes),percent crashes near (of total crashes),total bikes,total crashes
percentsPerBoxJan:	filledBoxesJan getPercents.awk
	gawk -f getPercents.awk Jan 

#lat,long,num crashes near bikes,num bikes near crashes,num crashes not near,num bikes not near
filledBoxesJan:	bikeBlobsJan manhatCrashJan Boxing.py boxCoords
	./Boxing.py Jan

#lat,long for all .005x.005 degree boxes in manhattan
boxCoords:	makeBoxes.py
	./makeBoxes.py

#"bike blob", date, start and end time for bike routes in manhattan
bikeBlobsJan:	bikeEndpointsJan bikeBubble.py
	./bikeBubble.py Jan

#start and end lat&long,date, start and end time
bikeEndpointsJan:	bikes.awk /data/raw/citiBike/2014/2014-01-CitiBiketripdata.gz
	./bikes.awk Jan

#lat,long,date,time of each car crash that happened in manhattan
manhatCrashJan:		vehicle.awk NYPD_Motor_Vehicle_Collisions.csv
	./vehicle.awk Jan


clean:
	rm manhattanBikeJan.pdf manhattanCrashJan.pdf manhattanTotBikeJan.pdf manhattanTotCrashJan.pdf \
	sortedPercentsBikeJan sortedPercentsCrashJan sortedPercentsTotBikeJan sortedPercentsTotCrashJan \
	percentsPerBoxJan filledBoxesJan boxCoords bikeBlobsJan bikeEndpointsJan manhatCrashJan
