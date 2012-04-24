<?php
require("dbinfo_user.php");

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
If(!checkdate($mm,$dd,$yy))
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
		      );
  return $salevalidity[$value];
}
function translateSaleType($value)
{ //https://cp.server272.com/resources/sysinfo.php states that we have up to php 5.3, not 5.4 ARrays in 5.4 don't need the "array suffix and use [] instead of ()
  $saletype=array(1=>"Land and Building",
		 2=>"Land only",
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
$query .=" and SALEDT > '$startdate' and SALEDT < '$enddate'";

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
  // ADD TO XML DOCUMENT NODE
  echo '<marker ';
  echo 'SALEDT="' . parseToXML($row['SALEDT']) . '" ';
  echo 'PARCELLOCATION="' . parseToXML($row['PARCELLOCATION']) . '" ';
  echo 'PARID="' . parseToXML($row['PARID']) . '" ';
  echo 'PRICE="' . money_format('%(#10n',$row['PRICE']) . '" ';
  echo 'SALETYPE="' . translateSaleType($row['SALETYPE']) . '" ';
  echo 'SALEVALIDITY="' . translateSaleValidity($row['SALEVALIDITY']) . '" ';
  echo 'Latitude="' . $row['Latitude'] . '" ';
  echo 'Longitude="' . $row['Longitude'] . '" ';
  echo '/>';
}

// End XML file
echo '</markers>';
// http://www.tizag.com/ajaxTutorial/ajax-mysql-database.php 
?>
