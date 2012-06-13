#!/bin/bash

#http://www.askdavetaylor.com/how_do_i_strip_leading_zeroes_for_math_in_a_shell_script.html

#the leading 000s appended to the price cause problems in gnuplot. It appears that gnuplot then interprets the numbers as something other than numbers (strings perhaps) and doesn't plot what is expected.

#awk uses 1 as 1st index (ie. non-zero indexing), -F, sets the filed delimiter as comma
#awk -F, '{print "%d\n", $4 }' "$1"  | sed 's/^0$//;/^$/d'

#this assumes that you want field 4 (which is the (sale)price field), the sed makes lines where the price is zero blank, and then it removes those blank lines.
awk -F, '{print $4 +0 }' "$1"  | sed 's/^0$//;/^$/d' > /tmp/prepforkde.txt
#capture the line count of the output file
numberofrecords=$( wc -l /tmp/prepforkde.txt | awk '{print $1}' )
echo "set autoscale; plot \"/tmp/prepforkde.txt\" using 1:(1./${numberofrecords}.) smooth kdensity; pause -1" > /tmp/plot.gnu
#to make the gnuplot stay on the screen, either add pause -1 to the file or call gnuplot
gnuplot /tmp/plot.gnu #-persist
