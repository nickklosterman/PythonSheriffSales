#!/bin/bash
HOST='djinnius.com'
USER="Split"
PASSWORD="UioP\$56&"
ftp -in $HOST <<'EOF'
user Split UioP$56&
binary 
mput SheriffSalesMapDynamic.html SheriffSalesMapDynamic.jquery.js   SheriffSalesMapDynamic.js SheriffSalesMapDynamic.css
quit
EOF
echo "done"

