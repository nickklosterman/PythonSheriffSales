#!/bin/bash
zipfilename="data\\Yearly\\SALES_2012.zip" 
csvfilename="SALES_2012_RES.csv"
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


wget "http://www.mctreas.org/data\Yearly\SALES_2012.zip" -v

unzip "data\\Yearly\\SALES_2012.zip" SALES_2012_RES.csv