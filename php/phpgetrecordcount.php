<?php
//I believe that we obtain the username, password adn database from this file
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

switch ($table) {
case  "RentalRegistrationMontgomeryCountyOhio":
$districtname=$_GET["districtname"];
$numberofunits=$_GET["numberofunits"];

$query = "SELECT count(*) AS num FROM $table WHERE DISTRICT_NAME = '$districtname' and NUMBER_OF_UNITS = ";
if (is_numeric($numberofunits))
$query .="'$numberofunits' ";

break;
case  "SheriffSalesMontgomeryCountyOhio":
$maxbid=$_GET["maxbid"];
$minbid=$_GET["minbid"];
$salestatus = $_GET["salestatus"];
$saledate = $_GET["saledate"];
$pricefiltercategory=$_GET["pricefiltercategory"];

//ignore these two for the record count
//$recordstodisplay=$_GET["recordstodisplay"];
//$recordsoffset=$_GET["recordsoffset"];

//escape user input to help prevent injection attacks
$maxbid = mysql_real_escape_string($maxbid);
$minbid = mysql_real_escape_string($minbid);
$minbid=parseCurrency($minbid);
$maxbid=parseCurrency($maxbid);
$pricefiltercategory=mysql_real_escape_string($pricefiltercategory);

//check that minbid/maxbid are in low->high and not vice versa
if ($minbid > $maxbid)
{  $temp=$maxbid;
$maxbid=$minbid;
$minbid=$temp;
}

$salestatus = mysql_real_escape_string($salestatus);
$saledate = mysql_real_escape_string($saledate);

//alias the count as a num so we can grab it 
$query = "SELECT count(*) AS num FROM $table WHERE $pricefiltercategory < ";
if (is_numeric($maxbid))
$query .="'$maxbid' and $pricefiltercategory >= "; //>= to capture values that are 0.
if (is_numeric($minbid))
$query .="'$minbid' ";
if ($salestatus!='*')
$query .=" and SaleStatus = '$salestatus' ";
if ($saledate!='*')
$query .=" and SaleDate = '$saledate' ";
break;
case  "RealEstateSalesMontgomeryCountyOhio":
break;

}


//debug statements
//$query="SELECT * FROM Property WHERE MinBid > 10 and MinBid < 100000000 and SaleStatus=\"Sold\" LIMIT 1,5";
//$query="SELECT * FROM Property WHERE MinBid > 10 and MinBid < 100000000 and SaleDate=2012-07-13 LIMIT 1,5";
//$query="SELECT * FROM Property WHERE MinBid > 10 and MinBid < 10000000 and SaleDate=2012-07-13 LIMIT $recordsoffset,$recordstodisplay ";
//$query="SELECT * FROM Property WHERE MinBid > 10 and MinBid < 10000000 and SaleDate=2012-07-13 LIMIT 0,7 ";
//echo $query ;

$result = mysql_query($query);
if (!$result) {
die('Invalid query: ' . mysql_error());
}

setlocale(LC_MONETARY, 'en_US');

header("Content-type: text/xml");


//since I'm only returning one xml tag do I need to 

//$num_rows=mysql_num_rows($result); //will this break the following use of $result
//echo '<recordCount="'. parseToXML($num_rows) . '" />';

$row = @mysql_fetch_assoc($result);
echo '<marker>' . PHP_EOL ;
echo '<data recordCount="'. parseToXML($row['num']) . '" />' . PHP_EOL ;
echo '<data2 query="' . parseToXML($query) . '" />' . PHP_EOL;
echo '</marker>' . PHP_EOL ;


// http://www.tizag.com/ajaxTutorial/ajax-mysql-database.php 
?>
