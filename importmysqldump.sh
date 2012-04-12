#!/bin/bash
echo "This will overwrite the contents of SheriffSales."
mysql -u nicolae -p SheriffSales < SheriffSalesDump.out

