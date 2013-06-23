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


//alias the count as a num so we can grab it 
$query = "SELECT count(*) AS num FROM $table ";

$result = mysql_query($query);
if (!$result) {
die('Invalid query: ' . mysql_error());
}

setlocale(LC_MONETARY, 'en_US');

header("Content-type: text/xml");

$row = @mysql_fetch_assoc($result);
echo '<marker>' . PHP_EOL ;
echo '<data recordCount="'. parseToXML($row['num']) . '" />' . PHP_EOL ;
echo '<data2 query="' . parseToXML($query) . '" />' . PHP_EOL;
echo '</marker>' . PHP_EOL ;


// http://www.tizag.com/ajaxTutorial/ajax-mysql-database.php 
?>
