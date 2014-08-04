<?php
//require("dbinfo_user.php");
require("../dbinfo_user.php");

function parseToXML($htmlStr) 
{ 
$xmlStr=str_replace('<','&lt;',$htmlStr); 
$xmlStr=str_replace('>','&gt;',$xmlStr); 
$xmlStr=str_replace('"','&quot;',$xmlStr); 
$xmlStr=str_replace("'",'&#39;',$xmlStr); 
$xmlStr=str_replace("&",'&amp;',$xmlStr); 
return $xmlStr; 
} 

function parseCurrency($htmlStr) 
{ 
$xmlStr=str_replace('$','',$htmlStr); 
$xmlStr=str_replace(',','',$xmlStr); 
return $xmlStr; 
} 

function validateDate($date) //the name was checkDate() but function names aren't case sensitive apparently
{ //http://www.plus2net.com/php_tutorial/date-validation.php
$arr=split("-",$date); // splitting the array
$yy=$arr[0]; // first element of the array is month
$mm=$arr[1]; // second element is date
$dd=$arr[2]; // third element is year
if(!checkdate($mm,$dd,$yy))
{
//echo "invalid date";
$output="2012-01-01";
}
else {
//echo "Entry date is correct";
$output=$date;
} 
return $output;
}

function translateSaleValidity($value)
{
$salevalidity=array(1=>"Valid Sale", 
2=>"Not Validated",
3=>"Related Individuals Or Corporations",
4=>"Liquidation/Foreclosure",
5=>"Not Open Market",
6=>"Partial Interest",
7=>"Land Contract or Unusual Financing",
8=>"Excess Personal PP or Not Arms Length",
9=>"Ownder Dishonesty in Description",
10=>"Sale Involving Multiple Parcels",
11=>"Invalid Date On Sale",
12=>"Outlier",
13=>"Property Changed After Sale",
14=>"Resale w/in 3 yrs",
15=>"Sale incl unlisted new const",
//		      11=>"",
);
return $salevalidity[$value];
}
function translateSaleType($value)
{ //https://cp.server272.com/resources/sysinfo.php states that we have up to php 5.3, not 5.4 ARrays in 5.4 don't need the "array suffix and use [] instead of ()
$saletype=array(1=>"Land and Building",
2=>"Land only",
3=>"Building only",
);
return $saletype[$value];
}

// Opens a connection to a MySQL server
$connection=mysql_connect (localhost, $username, $password);
if (!$connection) {
die('Not connected : ' . mysql_error());
}

// Set the active MySQL database
$db_selected = mysql_select_db($database, $connection);
if (!$db_selected) {
die ('Can\'t use db : ' . mysql_error());
}

//Build Query from input
$table=$_GET["table"];
switch ($table) {
case "RentalRegistrationMontgomeryCountyOhio":
$recordstodisplay=$_GET["recordstodisplay"];
$recordsoffset=$_GET["recordsoffset"];
$districtname=$_GET["districtname"];
$numberofunits=$_GET["numberofunits"];

$query = "SELECT PARCEL,LOCATION,NUMBER_OF_UNITS,Latitude,Longitude FROM $table ";
if ( $districtname!='*' )
{ 
$query .=" WHERE DISTRICT_NAME = '$districtname'";
if ( $numberofunits!='*')
$query .=" AND NUMBER_OF_UNITS = '$numberofunits'";
}
else
{
if ( $numberofunits!='*')
$query .=" WHERE NUMBER_OF_UNITS = '$numberofunits'";
}
break;

case "RealEstateSalesMontgomeryCountyOhio":
$maxbid=$_GET["maxbid"];
$minbid=$_GET["minbid"];
$saletype = $_GET["saletype"];
$salevalidity = $_GET["salevalidity"];
$startdate=$_GET["startdate"];
$enddate=$_GET["enddate"];
//escape user input to help prevent injection attacks
$maxbid = mysql_real_escape_string($maxbid);
$minbid = mysql_real_escape_string($minbid);
$minbid=parseCurrency($minbid);
$maxbid=parseCurrency($maxbid);
$startdate=validateDate($startdate);
$enddate=validateDate($enddate);
//check that minbid/maxbid are in low->high order and not vice versa
if ($minbid > $maxbid)
{  $temp=$maxbid;
$maxbid=$minbid;
$minbid=$temp;
}
$salestatus = mysql_real_escape_string($salestatus);
$saledate = mysql_real_escape_string($saledate);
// quote only values, not column name
$query = "SELECT * FROM $table WHERE PRICE < ";
if (is_numeric($maxbid))
$query .="'$maxbid' and PRICE >= "; //>= to capture values that are 0.
if (is_numeric($minbid))
$query .="'$minbid' ";
if ($saletype!='*')
$query .=" and SALETYPE = '$saletype' ";
if ($salevalidity!='*')
$query .=" and SALEVALIDITY = '$salevalidity' ";
$query .=" and SALEDT >= '$startdate' and SALEDT <= '$enddate'"; //>= and <= bc i think this is the expected behavior to include the chosen dates
break;

case "SheriffSalesMontgomeryCountyOhio":
$maxbid=$_GET["maxbid"];
$minbid=$_GET["minbid"];
$salestatus = $_GET["salestatus"];
$saledate = $_GET["saledate"];
$pricefiltercategory=$_GET["pricefiltercategory"];
$recordstodisplay=$_GET["recordstodisplay"];
$recordsoffset=$_GET["recordsoffset"];
//escape user input to help prevent injection attacks
$maxbid = mysql_real_escape_string($maxbid);
$minbid = mysql_real_escape_string($minbid);
$minbid=parseCurrency($minbid);
$maxbid=parseCurrency($maxbid);
$pricefiltercategory=mysql_real_escape_string($pricefiltercategory);
//$pricefiltercategory="MinBid";
//check that minbid/maxbid are in low->high and not vice versa
if ($minbid > $maxbid)
{  $temp=$maxbid;
$maxbid=$minbid;
$minbid=$temp;
}
$salestatus = mysql_real_escape_string($salestatus);
$saledate = mysql_real_escape_string($saledate);
// Select all the rows that meet our query
$query = "SELECT * FROM $table WHERE $pricefiltercategory < ";
if (is_numeric($maxbid))
//  $query .="'$maxbid' and MinBid > ";
$query .="'$maxbid' and $pricefiltercategory >= "; //>= to capture values that are 0.
if (is_numeric($minbid))
$query .="'$minbid' ";
if ($salestatus!='*')
$query .=" and SaleStatus = '$salestatus' ";
if ($saledate!='*')
$query .=" and SaleDate = '$saledate' ";
break;
}

if ( is_numeric($recordstodisplay) && is_numeric($recordsoffset) )
{
 if ( $recordsoffset >= 0 )
 { 
  if ( $recordstodisplay > 0 ) 
  {$query .=" LIMIT $recordsoffset,$recordstodisplay ";}
  else
  {  $query .="LIMIT 0,$recordstodisplay ";}
 }
}

$result = mysql_query($query);
if (!$result) {
die('Invalid query: ' . mysql_error());
}

setlocale(LC_MONETARY, 'en_US');

header("Content-type: text/xml");

// Start XML file, echo parent node
echo '<markers>';

// Iterate through the rows, printing XML nodes for each
while ($row = @mysql_fetch_assoc($result)){

switch ($table) {
case "RealEstateSalesMontgomeryCountyOhio":
// ADD TO XML DOCUMENT NODE
echo '<marker ';
echo 'SALEDT="' . parseToXML($row['SALEDT']) . '" ';
echo 'PARCELLOCATION="' . parseToXML($row['PARCELLOCATION']) . '" ';
echo 'PARID="' . parseToXML($row['PARID']) . '" ';
echo 'PRICE="' . money_format('%(#10n',$row['PRICE']) . '" ';
echo 'SALETYPE="' . translateSaleType($row['SALETYPE']) . '" ';
echo 'SALEVALIDITY="' . translateSaleValidity($row['SALEVALIDITY']) . '" ';
echo 'SALETYPEnum="' . parseToXML($row['SALETYPE']) . '" ';
echo 'SALEVALIDITYnum="' . parseToXML($row['SALEVALIDITY']) . '" ';
echo 'PRICEnum="' . parseToXML($row['PRICE']) . '" ';
echo 'Latitude="' . $row['Latitude'] . '" ';
echo 'Longitude="' . $row['Longitude'] . '" ';
echo '/>' . PHP_EOL;
break;

case "RentalRegistrationMontgomeryCountyOhio":
// ADD TO XML DOCUMENT NODE
echo '<marker ' . PHP_EOL ;
echo 'Parcel="' . parseToXML($row['PARCEL']) . '" ' . PHP_EOL ;
echo 'Location="' . parseToXML($row['LOCATION']) . '" ' . PHP_EOL ;
echo 'NumberOfUnits="' . parseToXML($row['NUMBER_OF_UNITS']) . '" ' . PHP_EOL ;
echo 'Latitude="' . $row['Latitude'] . '" ' . PHP_EOL ;
echo 'Longitude="' . $row['Longitude'] . '" ' . PHP_EOL ;
echo '/>' . PHP_EOL ;
break;

case "SheriffSalesMontgomeryCountyOhio":
// ADD TO XML DOCUMENT NODE
echo '<marker ' . PHP_EOL ;
echo 'SaleDate="' . parseToXML($row['SaleDate']) . '" ' . PHP_EOL ;
echo 'CaseNumber="' . parseToXML($row['CaseNumber']) . '" ' . PHP_EOL ;
echo 'Address="' . parseToXML($row['Address']) . '" ' . PHP_EOL ;
echo 'ZipCode="' . $row['ZipCode'] . '" ' . PHP_EOL ;
echo 'Plaintiff="' . parseToXML($row['Plaintiff']) . '" ' . PHP_EOL ;
echo 'Defendant="' . parseToXML($row['Defendant']) . '" ' . PHP_EOL ;
echo 'Attorney="' . parseToXML($row['Attorney']) . '" ' . PHP_EOL ;
echo 'SoldTo="' . parseToXML($row['SoldTo']) . '" ' . PHP_EOL ;
echo 'PID="' . parseToXML($row['PID']) . '" ' . PHP_EOL ;
echo 'Appraisal="' . money_format('%(#10n',$row['Appraisal']) . '" ' . PHP_EOL ;  
echo 'MinBid="' . money_format('%(#10n',$row['MinBid']) . '" ' . PHP_EOL ;
echo 'SaleAmt="' . money_format('%(#10n',$row['SaleAmt']) . '" ' . PHP_EOL ;
echo 'SaleStatus="' . parseToXML($row['SaleStatus']) . '" ' . PHP_EOL ;
echo 'Latitude="' . $row['Latitude'] . '" ' . PHP_EOL ;
echo 'Longitude="' . $row['Longitude'] . '" ' . PHP_EOL ;
echo '/>' . PHP_EOL ;
break;
}
}

// End XML file
echo '</markers>';
// http://www.tizag.com/ajaxTutorial/ajax-mysql-database.php 
?>
