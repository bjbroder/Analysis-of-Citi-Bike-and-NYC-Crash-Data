#!/usr/bin/gawk -f 

function isPointInPath(x, y,   poly,num,i,j,c){

    poly[1][1] = -74.012344
    poly[1][2] = 40.705452
    poly[2][1] = -74.005992
    poly[2][2] = 40.751633
    poly[3][1] = -73.926856
    poly[3][2] = 40.87363
    poly[4][1] = -73.912094
    poly[4][2] = 40.872332
    poly[5][1] = -73.936126
    poly[5][2] = 40.836496
    poly[6][1] = -73.932693
    poly[6][2] = 40.797782
    poly[7][1] = -73.976982
    poly[7][2] = 40.736677
    poly[8][1] = -73.980071
    poly[8][2] = 40.71326

    num = length(poly) + 1
    j = num - 1
    c = 0
    for (i=1; i<num; i++)
    {
	if (((poly[i][2] > y) != (poly[j][2] > y)) &&  
	   (x < poly[i][1] + (poly[j][1] - poly[i][1]) * (y - poly[i][2]) / (poly[j][2] - poly[i][2])))
	    c = 1- c
	j = i
    }
    return c
}

BEGIN{

    FS = ","
    OFS = ","

    fout = "manhatCrash" ARGV[1] #outputes to either "manhatCrashJan" or "manhatCrashYear" depnding on input 
    
    file = "NYPD_Motor_Vehicle_Collisions.csv"
    while (getline < file)
    {
	date = $1
	split(date,a,"/")
	loc =  $5 "|" $6 #this concats the lat and long and goes around awk's auto-casting so that if 5 and 6 are empty there will still be a "|"

	if ((ARGV[1] == "Jan" && a[1] == "01") || ARGV[1] == "Year") #either doing Jan file in which case must be Jan data or Year file and can be any month
	{
	    if (a[3] == 2014 && loc != "|") #checks year and makes sure lat and long are not both empty
	    {
		if (isPointInPath($6,$5)) #checks if crash occured in mahattan)
		{
		    print $6, $5, $1, $2  >> fout #outputs: crash's long, lat, date, time
		}
	    }
	}
    }

    close(file)


}
