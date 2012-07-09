#!/bin/bash
function getFileExtension()
{
    extension1=${1##*.}
    extension=${extension1,,} #convert to all lower case                                                                                                                                                     
    echo "$extension"
}
function getFileName()
{
    filename=${1%.*}
    echo "$filename"
}

function createUniqueFilename()
{
    filename="${1}"
#    filenamebase=${filename%.*}
#    filenameextension=${filename#*.}
    filenamebase=$( getFileName $filename )
    filenameextension=$( getFileExtension $filename )
    temp=$filenamebase.$filenameextension
    number=0
    
    while [[ -e "$filename" ]]
    do
#	echo $number
        let 'number+=1'
        numberformat=$( printf "%02d" $number )
        filename=${filenamebase}_$numberformat.${filenameextension}
    done
    touch "$filename" #needed more for 
    echo "$filename"
}

dbuserLocal="nicolae"
dbuserRemote="djinnius"
todaysdate=`date +%F`
if [ $# -ne 1 ]
then
    outputfilename="SheriffSales-$todaysdate.out"
else 
    outputfilename="$1"
fi


#getFileExtension $outputfilename
#getFileName $outputfilename


#createUniqueFilename $outputfilename 
outputfilename=$( createUniqueFilename $outputfilename )

if [ 0 -eq 1 ]
then #old method of preventing filename collisions
    while [ -e $outputfilename ]
    do 	
	echo "$outputfilename exists. \nPlease enter an alternate output filename:"
	read outputfilename
	
    done
fi

echo "Writing database dump to $outputfilename"
if [ 0 -eq 1 ]
then
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
fi