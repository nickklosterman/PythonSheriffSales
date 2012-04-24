#!/bin/bash
#mysql -u Nottingham -p djinnius_SheriffSales -h mysql.server272.com -P 3306 < SheriffSalesDumpWPA.out 
#Enter password: 
#ERROR 1142 (42000) at line 22: DROP command denied to user 'Nottingham'@'76.243.46.202' for table 'PennsylvaniaProperty'

if [ $# -ne 1 ]
then
    echo "Please specify a databse to upload."
else
    databasedump="$1"
    mysql -u djinnius -p djinnius_SheriffSales -h mysql.server272.com -P 3306 < "$databasedump"
    echo "uploading database $databasedump"
fi
#have to do it as djinnius bc otherone doesn't have drop acces...could easily change..
