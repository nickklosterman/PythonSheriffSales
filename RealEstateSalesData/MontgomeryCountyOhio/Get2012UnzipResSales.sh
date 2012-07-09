#!/bin/bash
zipfilename="data\\Yearly\\SALES_2012.zip" SALES_2012_RES.csv
csvfilename="SALES_2012_RES.csv"
if [ -e $zipfilename ]
then
rm $zipfilename
fi

if [ -e $csvfilename ]
then
rm $csvfilename 
fi


wget "http://www.mctreas.org/data\Yearly\SALES_2012.zip" -v

unzip "data\\Yearly\\SALES_2012.zip" SALES_2012_RES.csv