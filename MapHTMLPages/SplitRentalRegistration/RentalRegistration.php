<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <title>Montgomery County Sheriff Sales</title>
    <link rel="stylesheet" type="text/css" href="RentalRegistration.css" />
    <script src="http://maps.google.com/maps/api/js?sensor=false" type="text/javascript"></script>
    <script type="text/javascript" src="jquery-1.8.0.min.js"></script>
    <script src="RentalRegistration.js"></script>
    <script src="RentalRegistration.jquery.js"></script>
  </head>
  <body>
    <div id="Menu">
      <div id="select-column">
  <div id="select-row">
          <label>District:</label>
          <select onchange="updateMap()" id='taxdistrict'>
            <option value="*" selected>All</option>
        <?php
             //specifies username,password,database, and table
             require("../dbinfo_user.php");
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
             $sql="select distinct(DISTRICT_NAME) from RentalRegistrationMontgomeryCountyOhio2013 order by DISTRICT_NAME asc"; //
//             echo $sql;
             $rs=mysql_query($sql);
             while($row = mysql_fetch_array($rs))
             {
             echo "<option value=\"".$row['DISTRICT_NAME']."\">".$row['DISTRICT_NAME']."</option>\n  ";
             }
             ?>

          </select>
        </div>

  <div id="select-row">
          <label>Units:</label>
          <select onchange="updateMap()" id='taxdistrict'>
            <option value="*" selected>All</option>
        <?php
             //specifies username,password,database, and table
             require("../dbinfo_user.php");
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
             $sql="select distinct(NUMBER_OF_UNITS) from RentalRegistrationMontgomeryCountyOhio2013 order by NUMBER_OF_UNITS asc"; //
//             echo $sql;
             $rs=mysql_query($sql);
             while($row = mysql_fetch_array($rs))
             {
             echo "<option value=\"".$row['NUMBER_OF_UNITS']."\">".$row['NUMBER_OF_UNITS']."</option>\n  ";
             }
             ?>

          </select>
        </div>



	<div id="select-row">
	  <label> Number of Records To Display:</label>
	  <select onchange="updateMap()" id="recordstodisplay">
	    <option>10</option>
	    <option selected>25</option>
	    <option>50</option>
	    <option>75</option>
	    <option>100</option>
	    <option>150</option>
	    <option>200</option>
	    <option>250</option>
	    <option>500</option>
	  </select>
	</div>

	<div id="select-row">
	  <span id="dec">
	    <button id="decrementOffset">  <-= </button>
					       </span>
	  <span id="inc">
	    <button id="incrementOffset"> =->   </button>
	  </span>
	</div>
      </div>
      <div id="select-row">
	<label id="CurrentRecordsDisplayed"></label>
      </div>

    </div>
    <div id="map" style="width: 100%; height: 85%"></div>
  </body>
</html>
