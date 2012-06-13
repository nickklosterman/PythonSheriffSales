#!/bin/bash
mysql -u nicolae -p SheriffSales -e "select distinct(saledate) from Property order by saledate desc" | grep '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}'