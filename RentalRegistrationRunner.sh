#!/bin/bash

cd RentalRegistration/MontgomeryCountyOhio/
bash Get2013UnzipRentalRegistration.sh
cd ../../
python3 RentalRegistrationMontgomeryCountyOhio2013.py
