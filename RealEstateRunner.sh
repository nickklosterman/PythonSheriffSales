#!/bin/bash
cd ~/Git/PythonSheriffSales/RealEstateSalesData/MontgomeryCountyOhio

year=` date +%Y `

bash GetXUnzipResSales.sh $year

cd ~/Git/PythonSheriffSales/
python2 ProcessRealEstateSalesMontgomeryCountyOhio2014.py

cd ~/Git/PythonSheriffSales/Geocoders 
python2 UnifiedGeocoder.py -t RealEstateSalesMontgomeryCountyOhio2014 -l  ~/.mysqllogin_rentalreg
#python2 GeocodeRealEstateDatabase2014.py
