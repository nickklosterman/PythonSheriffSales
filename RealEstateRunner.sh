#!/bin/bash
cd ~/Git/PythonSheriffSales/RealEstateSalesData/MontgomeryCountyOhio
#bash Get2013UnzipResSales.sh
year=` date +%Y `

 bash GetXUnzipResSales.sh $year

 cd ~/Git/PythonSheriffSales/
 python2 ProcessRealEstateSalesMontgomeryCountyOhio2014.py

cd ~/Git/PythonSheriffSales/Geocoders 
python2 GeocodeRealEstateDatabase2014.py
