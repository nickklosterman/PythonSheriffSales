#!/bin/bash
dbuser="nicolae"

if [ $# -ne 1 ]
then
    outputfilename="SheriffSalesDumpLatest.out"
else 
    outputfilename="$1"
fi
while [ -e $outputfilename ]
do 
    echo "$outputfilename exists. \nPlease enter an alternate output filename:"
    read outputfilename
done

echo "Writing database dump to $outputfilename"

echo "Logging into the local database as $dbuser."
mysqldump -u "$dbuser" -p SheriffSales > "$outputfilename"
