startyear=2000
while [ $startyear -lt 2013 ]
do
echo "wget http://www.mctreas.org/data\Yearly\SALES_${startyear}.zip"
wget "http://www.mctreas.org/data\Yearly\SALES_${startyear}.zip" -nv
let 'startyear+=1'
done