#!/bin/bash
outputfilename="SheriffSalesDumpLatest.out"
while [ -e $outputfilename ]
do 
echo "$outputfilename exists. \nPlease enter an alternate output filename:"
read outputfilename
done
 
echo "Writing database dump to $outputfilename"

mysqldump -u nicolae -p SheriffSales > "$outputfilename"
