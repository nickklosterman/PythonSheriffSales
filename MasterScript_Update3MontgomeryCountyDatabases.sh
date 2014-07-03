#!/bin/bash
bash RentalRegistrationRunner.sh
bash GetLatestSheriffSalesList.sh
bash RealEstateRunner.sh
bash DatabaseUtil/dumpSheriffSalesDBAndUploadtoDjinniusLocalDatabase.sh
