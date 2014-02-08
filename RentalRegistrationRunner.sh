#!/bin/bash

cd RentalRegistration/MontgomeryCountyOhio/
bash Get2013UnzipRentalRegistration.sh #the data on the website seems to be year agnostic
cd ../../
python3 RentalRegistrationMontgomeryCountyOhio2014.py
cd Geocoders
python GeocodeRentalRegistration2014.py
