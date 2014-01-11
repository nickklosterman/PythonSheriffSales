#!/bin/bash

# This script get the latest sheriff sales from the Montgomery Cty Ohio website and saves it. The daterange is used to create a unique filename. If the date range is taken then an integer is appended to the end of the filename to make the filename unique

function getFileExtension()
{
    extension1=${1##*.}
    extension=${extension1,,} #convert to all lower case                                                                            
    #the above doesn't  work correctly on files with spaces in them
    # I therefore renamed the input file so there were no spaces
    # http://linuxgazette.net/18/bash.html for the ${Variable##*.} syntax 

    echo "$extension"
}
function getFileName()
{
    filename=${1%.*}
    filename=`basename  ${1} .htm`
    echo "$filename"
}

function createUniqueFilenameWithDates()
{
    filename="${1}"
    startDate="${2}"
    endDate="${3}"
    filenamebase=$( getFileName $filename )
    filenameextension=$( getFileExtension $filename )
    temp=$filenamebase${startDate}${endDate}.$filenameextension
    number=0
    
    filename=${filenamebase}${startDate}${endDate}.${filenameextension} 
    while [[ -e "$filename" ]]
    do
        let 'number+=1'
        numberformat=$( printf "%02d" $number )
        filename=${filenamebase}${startDate}${endDate}_$numberformat.${filenameextension} #when I was using startdate and enddate, it seemed that they were somehow referencing the global variables and not the local ones. 
    done
    touch "$filename" #needed more for 
    echo "$filename"
}


wget http://www.mcohio.org/sheriff/sflistauction.cfm -O /tmp/sflistauction.cfm

startdate=`grep idate2 /tmp/sflistauction.cfm | sed -e 's/^.*value="//;s/".*//'`
enddate=`grep idate2 /tmp/sflistauction.cfm | sed -e 's/^.*value="//;s/".*//'`

startdate=`grep idate1 /tmp/sflistauction.cfm | sed -e 's/^.*value="//;s/".*//;s/\//%2F/g'` #remove / and replace with %2F for 
enddate=`grep idate2 /tmp/sflistauction.cfm | sed -e 's/^.*value="//;s/".*//;s/\//%2F/g'` #remove / and replace with %2F for 

startdateForFilename=`grep idate1 /tmp/sflistauction.cfm | sed -e 's/^.*value="//;s/".*//;s/\///g'` # remove / and replace w nothing
enddateForFilename=`grep idate2 /tmp/sflistauction.cfm | sed -e 's/^.*value="//;s/".*//;s/\///g'` # remove / and replace w nothing

filename="Sheriff Sales List.htm"
filename="Sheriff_Sales_List.htm"

outputFileName=$(createUniqueFilenameWithDates "${filename}" ${startdateForFilename} ${enddateForFilename})


echo "$outputFileName"

curl -d "idate1=${startdate}&idate2=${enddate}&iSUMDET=DET" http://www.mcohio.org/sheriff/sflistauctiondo.cfm > "${outputFileName}"


python SheriffSaleProcessors/SheriffSalesLinkCreatorMontgomeryCountyOhio_Detailed.py "${outputFileName}"

#python Geocoders/GeocodeDatabase.py

