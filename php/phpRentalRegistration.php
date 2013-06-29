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
$table=$_GET["table"];
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

header("Content-type: text/xml");

// Start XML file, echo parent node
echo '<markers>' . PHP_EOL ;
echo '<item' . PHP_EOL . ' query="' . parseToXML($query) . '"' . PHP_EOL .' />' . PHP_EOL ;
// Iterate through the rows, printing XML nodes for each
while ($row = @mysql_fetch_assoc($result)){
// ADD TO XML DOCUMENT NODE
echo '<marker ' . PHP_EOL ;
echo 'Parcel="' . parseToXML($row['PARCEL']) . '" ' . PHP_EOL ;
echo 'Location="' . parseToXML($row['LOCATION']) . '" ' . PHP_EOL ;
echo 'NumberOfUnits="' . parseToXML($row['NUMBER_OF_UNITS']) . '" ' . PHP_EOL ;
echo 'Latitude="' . $row['Latitude'] . '" ' . PHP_EOL ;
echo 'Longitude="' . $row['Longitude'] . '" ' . PHP_EOL ;
echo '/>' . PHP_EOL ;
}

// End XML file
echo '</markers>' . PHP_EOL ;
// http://www.tizag.com/ajaxTutorial/ajax-mysql-database.php 
?>
