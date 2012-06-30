<?php
//specifies username,password,database, and table
require("dbinfo_user.php"); 
// Opens a connection to a MySQL server
   $connection=mysql_connect (localhost, $username, $password);
   if (!$connection) {
   die('Not connected : ' . mysql_error());
   }

// Set the active MySQL database
   $db_selected = mysql_select_db($database, $connection); 
//could I possibly have a diff dbinfo_user.php that specifies the table to use? YES!!
   if (!$db_selected) {
   die ('Can\'t use db : ' . mysql_error());
			  }
//$sql="select distinct(SaleDate) from Property where not zipcode=\"0\" order by SaleDate desc"; //doesn't work
$sql="select distinct(SaleDate) from Property order by SaleDate desc"; //works
//$sql="select distinct(SaleDate) from Property where not zipcode="0" order by SaleDate desc"; // phail
//$sql="select distinct(SaleDate) from Property where not zipcode=""0"" order by SaleDate desc"; // phail
$sql="select distinct(SaleDate) from Property where not zipcode=0 order by SaleDate desc"; //
//echo $sql;
echo "<select id='yoyo'>\n";
$rs=mysql_query($sql);
while($row = mysql_fetch_array($rs))
  {
    //I can't figure out why but the option html tag isn't being written out. WHY!!?? It was being written out but even thogh prev I hadn't wrapped the results in a <select> tag, FFox was reading it as html and not displaying the tag
    //    echo " \<option\> " . $row['SaleDate'] . " </option> \n";
    //echo " <option\> </option> \n";
    //Echo " <option\> $row['SaleDate']  </option> \n"; // fail
    //    Echo "stuff1" . $row['SaleDate'] . "buff \n ";  //is there a diff btw echo and Echo??
    echo "<option value=\"".$row['SaleDate']."\">".$row['SaleDate']."</option>\n  ";
    //    Print " \<option\> " . $row['SaleDate'] . " </option> \n";
  }
echo "</select>";
//echo 'foshizzle nigga';
// echo $username; echo $password; echo $table; echo $database; //how to prevent this from being displayed.

// This won't work because of the quotes around specialH5!
//echo "<h5 class="specialH5">I love using PHP!</h5>";  

// OK because we escaped the quotes!
echo "<h5 class=\"specialH5\">I love using PHP!</h5>";  

// OK because we used an apostrophe '
echo "<h5 class='specialH5'>I love using PHP!</h5>";  

?>