#!/bin/bash
HOST='djinnius.com'
USER="Split"
PASSWORD="UioP\$56&"
ftp -in $HOST <<'EOF'
user Split UioP$56&
binary
mput Map.html Unified.js Unified.jQuery.js 
quit
EOF
echo "done"
