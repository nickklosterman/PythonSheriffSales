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
$salestatus = $_GET["salestatus"];
$saledate = $_GET["saledate"];
$pricefiltercategory=$_GET["pricefiltercategory"];
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
//$query = "SELECT * FROM Property WHERE MinBid < ";
//$query = "SELECT * FROM Property WHERE '$pricefiltercategory' < "; // <-- this won't work. we don't want to quote our column name, only values
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


$result = mysql_query($query);
if (!$result) {
  die('Invalid query: ' . mysql_error());
}

setlocale(LC_MONETARY, 'en_US');

header("Content-type: text/xml");

// Start XML file, echo parent node
echo '<markers>';

//output recordcount header
$num_rows=mysql_num_rows($result); //will this break the following use of $result
echo '<marker recordCount="'. parseToXML($num_rows) . '" />' . PHP_EOL;

// Iterate through the rows, printing XML nodes for each
while ($row = @mysql_fetch_assoc($result)){
  // ADD TO XML DOCUMENT NODE
  echo '<marker ' . PHP_EOL;
  echo 'SaleDate="' . parseToXML($row['SaleDate']) . '" ' . PHP_EOL;
  echo 'CaseNumber="' . parseToXML($row['CaseNumber']) . '" ' . PHP_EOL;
  echo 'Address="' . parseToXML($row['Address']) . '" ' . PHP_EOL;
  echo 'ZipCode="' . $row['ZipCode'] . '" ' . PHP_EOL;
  echo 'Plaintiff="' . parseToXML($row['Plaintiff']) . '" ' . PHP_EOL;
  echo 'Defendant="' . parseToXML($row['Defendant']) . '" ' . PHP_EOL;
  echo 'Attorney="' . parseToXML($row['Attorney']) . '" ' . PHP_EOL;
  echo 'SoldTo="' . parseToXML($row['SoldTo']) . '" ' . PHP_EOL;
  echo 'PID="' . parseToXML($row['PID']) . '" ' . PHP_EOL;
  echo 'Appraisal="' . money_format('%(#10n',$row['Appraisal']) . '" ' . PHP_EOL;  
  echo 'MinBid="' . money_format('%(#10n',$row['MinBid']) . '" ' . PHP_EOL;
  echo 'SaleAmt="' . money_format('%(#10n',$row['SaleAmt']) . '" ' . PHP_EOL;
  echo 'SaleStatus="' . parseToXML($row['SaleStatus']) . '" ' . PHP_EOL;
  echo 'Latitude="' . $row['Latitude'] . '" ' . PHP_EOL;
  echo 'Longitude="' . $row['Longitude'] . '" ' . PHP_EOL;
  echo '/>' . PHP_EOL;
}

// End XML file
echo '</markers>';
// http://www.tizag.com/ajaxTutorial/ajax-mysql-database.php 
?>
