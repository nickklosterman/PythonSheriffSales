#!/bin/bash
cd ~/Git/PythonSheriffSales/RealEstateSalesData/MontgomeryCountyOhio

year=` date +%Y `
inputfile=RealEstateSalesData/MontgomeryCountyOhio/SALES_${year}_RES.csv
echo ${inputfile}

bash GetXUnzipResSales.sh $year

cd ~/Git/PythonSheriffSales/
#the script is really year agnostic. The data goes into a db that doesn't have a year associated with it
python2 ProcessRealEstateSalesMontgomeryCountyOhio2014.py -input ${inputfile}

cd ~/Git/PythonSheriffSales/Geocoders 
python2 UnifiedGeocoder.py -t RealEstateSalesMontgomeryCountyOhio -l  ~/.mysqllogin_rentalreg
#python2 GeocodeRealEstateDatabase2014.py
