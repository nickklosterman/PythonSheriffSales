#!/bin/bash
HOST='djinnius.com'
USER="Split"
PASSWORD="UioP\$56&"
ftp -in $HOST <<'EOF'
user Split UioP$56&
binary
#mput RentalRegistration.html RentalRegistration.jquery.js   RentalRegistration.js RentalRegistration.css RentalRegistration.php
mput RentalRegistration.jquery.js   RentalRegistration.js RentalRegistration.css RentalRegistration.php
quit
EOF
echo "done"
