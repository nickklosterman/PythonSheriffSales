#!/bin/bash
#the regexp for the grep only returns the mathched expression and not the formatting bars from ysql
mysql -u nicolae -p SheriffSales -e "select distinct(saledate) from Property where not zipcode=\"0\" order by saledate desc ;" | grep '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}'  | sed 's/^/\<option\>/;s/$/\<\/option\>/'
