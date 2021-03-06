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
$maxbid = $_GET['maxbid']
$minbid = $_GET['minbid']
$salestatus = $_GET['salestatus']
$saledate = $_GET['saledate']

// Select all the rows in the markers table
$query = "SELECT * FROM Property WHERE 1";
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
  echo 'SaleDate="' . parseToXML($row['SaleDate']) . '" ';
  echo 'CaseNumber="' . parseToXML($row['CaseNumber']) . '" ';
  echo 'Address="' . parseToXML($row['Address']) . '" ';
  echo 'ZipCode="' . $row['ZipCode'] . '" ';
  echo 'Plaintiff="' . parseToXML($row['Plaintiff']) . '" ';
  echo 'Defendant="' . parseToXML($row['Defendant']) . '" ';
  echo 'Attorney="' . parseToXML($row['Attorney']) . '" ';
  echo 'SoldTo="' . parseToXML($row['SoldTo']) . '" ';
  echo 'PID="' . parseToXML($row['PID']) . '" ';
  echo 'Appraisal="' . money_format('%(#10n',$row['Appraisal']) . '" ';  
  echo 'MinBid="' . money_format('%(#10n',$row['MinBid']) . '" ';
  echo 'SaleAmt="' . money_format('%(#10n',$row['SaleAmt']) . '" ';
  echo 'SaleStatus="' . parseToXML($row['SaleStatus']) . '" ';
  echo 'Latitude="' . $row['Latitude'] . '" ';
  echo 'Longitude="' . $row['Longitude'] . '" ';
  echo '/>';
}

// End XML file
echo '</markers>';

?>
