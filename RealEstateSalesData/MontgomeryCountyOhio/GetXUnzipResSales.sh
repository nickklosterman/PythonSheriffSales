#!/bin/bash
inputYear=$1
zipfilename="data\\Yearly\\SALES_${1}.zip" 
csvfilename="SALES_${1}_RES.csv"
if [ -e "$zipfilename" ]
then
    rm "$zipfilename"
else
echo "nope"
fi

if [ -e "$csvfilename" ]
then
    rm "$csvfilename"
else
echo "nope2"
fi


wget "http://www.mctreas.org/data\Yearly\SALES_${1}.zip" -v

unzip "data\\Yearly\\SALES_${1}.zip" SALES_${1}_RES.csv