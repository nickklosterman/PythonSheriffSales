#!/bin/bash

zipfilename="rentalreg_list.zip"
csvfilename="rentalreg_A011.csv" 

#if there is the first csv file assume they are all present and delete them.
if [ -e "$csvfilename" ]
then
    
    echo "About to delete all csv files! press a key to continue"
    read somekey
    rm rentalreg_*.csv
else
echo "nope2"
fi

echo "Getting Rental Registration file"
wget http://www.mcohio.org/government/auditor/docs/rentalreg_list.zip
echo "unzipping list"
unzip rentalreg_list.zip 

myDate=`date +%F`
echo "moving file to rentalreg_list.${myDate}.zip"
mv rentalreg_list.zip rentalreg_list.${myDate}.zip 
