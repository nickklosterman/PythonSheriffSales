#!/bin/bash
echo "This will overwrite the contents of SheriffSales."
if [ $# -ne 1 ]
then
    outputfilename="SheriffSalesDumpLatest.out"
else 
    outputfilename="$1"
fi

mysql -u nicolae -p SheriffSales < "$outputfilename"

