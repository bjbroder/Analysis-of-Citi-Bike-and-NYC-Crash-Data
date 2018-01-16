#!/usr/bin/gawk -f

BEGIN{
    FS = "|"
    OFS = ","

    

    if (ARGV[1] == "Jan") #if doing Jan file, only Jan data as the only element in file list
    {
	file[1] = "/data/raw/citiBike/2014/2014-01-CitiBiketripdata.gz"
    }

    else #if year file, loop through and make the file list have 12 elements
    {
	for(i = 1; i <= 12; i++)
	{
	    if (i < 10)
		file[i] = "/data/raw/citiBike/2014/2014-0" i "-CitiBiketripdata.gz"
	    else if (i != 12)
		file[i] = "/data/raw/citiBike/2014/2014-" i "-CitiBiketripdata.gz"
	    else
		file[i] = "/data/raw/citiBike/2014/2014-" i "-CitiBoketripdata.gz"
	                        #bike was spelled wrong in the december file name so 12 was separated
	}
    }
    output = "bikeEndpoints" ARGV[1] #outputs to either "bikeEndpointsJan" or "bikeEndpointsYear" based on input
    for(i = 1; i <= length(file); i++)
    {
	command = "zcat " file[i] #unzips the i-th file in file list
	while (command | getline)
        {
	    if ($7 ~/[0-9]+$/) #makes sure long has a value (some where missing)
	    {
		split($2,start," ") #start[1] is the start date, start[2] is the start time
		split($3,end," ") #end[1] is the end date, end[2] is the end time
		#ignoring end date - assumming routes occur within one day)

		if (i >= 9) #file format changes starting in september; instead of yyyy-mm-dd changed to mm/dd/yyyy
		{
		    split(start[1],d,"/") #splits date on /
		    if (i==9)
		    {
			date = "09" "/" d[2] "/" d[3] #the 9 was missing its leading 0 so it is manually added back
		    }
		    else
		    {
			date = d[1] "/" d[2] "/" d[3]
		    }
			
		}
		else
		{
		    split(start[1],d,"-") #splits date on -
		    date = d[2] "/" d[3] "/" d[1]

		}
		split(start[2],t1,":")
		split(end[2],t2,":")

		time1 = t1[1] ":" t1[2] #takes only the hours and minutes of start time
		time2 = t2[1] ":" t2[2] #takes only the hours and minutes of end time

		print $6, $7, $10, $11, date, time1, time2 >> output
	    }
	}
	close(file[i]) #closes each file when it it done being used
    }

}
