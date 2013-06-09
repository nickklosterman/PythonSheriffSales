#!/bin/bash
cd ~/Git/PythonSheriffSales/RealEstateSalesData/MontgomeryCountyOhio
bash Get2013UnzipResSales.sh
cd ~/Git/PythonSheriffSales/
python ProcessRealEstateSalesMontgomeryCountyOhio2013.py
cd ~/Git/PythonSheriffSales/Geocoders 
python GeocodeRealEstateDatabase.py