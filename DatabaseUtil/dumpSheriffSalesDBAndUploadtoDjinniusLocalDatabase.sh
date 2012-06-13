#!/bin/bash
dbuserLocal="nicolae"
dbuserRemote="djinnius"
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

echo "Logging into the local database as $dbuserLocal."
mysqldump -u "$dbuserLocal" -p SheriffSales > "$outputfilename"

#mysql -u Nottingham -p djinnius_SheriffSales -h mysql.server272.com -P 3306 < SheriffSalesDumpWPA.out 
#Enter password: 
#ERROR 1142 (42000) at line 22: DROP command denied to user 'Nottingham'@'76.243.46.202' for table 'PennsylvaniaProperty'
if [ -e "$outputfilename" ]
then 
    echo "Logging into the remote database as $dbuserRemote."
    mysql -u "$dbuserRemote" -p djinnius_SheriffSales -h mysql.server272.com -P 3306 < "$outputfilename"
    echo "uploading database $outputfilename"
fi
#have to do it as djinnius bc otherone doesn't have drop acces...could easily change..