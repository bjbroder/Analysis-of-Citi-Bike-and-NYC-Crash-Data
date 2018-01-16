#!/usr/bin/gawk -f

BEGIN {

    FS = "|"
    OFS = "|"
    
    fin = "filledBoxes" ARGV[1]

    fout = "percentsPerBox" ARGV[1]
    
    while (getline < fin)
    {
#	what percent of bikes were near crashes
	totBikes = $4 + $6
	if (totBikes != 0)  {percentBikes = (($4 / totBikes) * 100)}
	else                {percentBikes = 0}      #avoids division by 0

#	what percent of crashes were near bikes
	totCrashes = $3 + $5
	if (totCrashes != 0)  {percentCrashes = ($3 / totCrashes) * 100}
	else                  {percentCrashes = 0}  #avoids division by 0
	
	print $0 "|" percentBikes "|" percentCrashes "|" totBikes "|" totCrashes >> fout

    }

}
