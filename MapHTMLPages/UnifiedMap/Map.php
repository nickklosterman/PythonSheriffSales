<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <title>Montgomery County Real Estate Sales</title>
    <script src="http://maps.google.com/maps/api/js?sensor=false" type="text/javascript"></script>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    <script type="text/javascript" src="Unified.jQuery.js"></script>
    <script type="text/javascript" src="Unified.js"></script>
    <style>
      #SheriffSales { display:inline}
      #RealEstateSales { display:none }
      #RentalRegistration { display:none }
    </style>

  </head>

  <!-- <body onload="Mapfunction('SheriffSales',false)"> I think this was making the double call -->
<body>
    <div id="radio">
      <input id="radio1" type="radio" name="radio" checked="checked"><label for="radio1">Sheriff Sales</label>
      <input id="radio2" type="radio" name="radio"><label for="radio2">Real Estate Sales</label>
      <input id="radio3" type="radio" name="radio"><label for="radio3">Rental Registration </label>
    </div>
    <div id="SheriffSales">
      <div id="Menu">
	    <select onchange="Mapfunction('SheriffSales',true)" id='pricefiltercategory'>
	      <option value="MinBid">Minimum Bid</option>
	      <option value="Appraisal">Appraisal Amount</option>
	      <option value="SaleAmt">Sale Amount</option>
	    </select>
	    <!--
		http://www.skytopia.com/project/articles/compsci/form.html how to dynamically execute according to which list/dropdown/radio is selected.
		Minimum Bid
	      -->
	    <label>between</label>
	    $<input type='text' id='minbid' value='1,000' />
	    <label>and</label>
	    $<input type='text' id='maxbid' value='2,000,000' />
	    <div>
	    <label>Sale Status:</label>
	    <select onchange="Mapfunction('SheriffSales',true)" id='salestatus'>
	      <option value="*" selected>All</option>
	      <option>Active</option>
	      <option>Sold</option>
	      <option>Cancelled</option>
	      <option>No Bid, No Sale</option>
	    </select>
	    <label>Sale Date:</label>
	    <select onchange="Mapfunction('SheriffSales',true)" id='saledate'>
	      <option value="*" selected>All</option>
              <?php  //For these php sections to work, you have to have the file named .php, not .html etc.
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
		 $sql="select distinct(SaleDate) from SheriffSalesMontgomeryCountyOhio where not zipcode=0 order by SaleDate desc"; //
		 //             echo $sql;
		 $rs=mysql_query($sql);
		 while($row = mysql_fetch_array($rs))
		 {
		 echo "<option value=\"".$row['SaleDate']."\">".$row['SaleDate']."</option>\n  ";
		 //  echo '<option>'.$row['SaleDate'].'</option>\n';
		 }
		 ?>

	    </select>
	    <label>Info Window:</label>
	    <select onchange="Mapfunction('SheriffSales',true)" id='infowindow'>
	      <!--   onChange="updateMap3()"> -->
	      <option >Detailed</option>
	      <option >Summary</option>
	    </select>

	    <label> Number of Records To Display:</label>
	    <select onchange="Mapfunction('SheriffSales',true)" id="recordstodisplay">
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
	  <!-- I could add an image here. there are multiple options now: css,svg,canvas
	       http://www.scriptol.com/html5/button.php
	       http://croczilla.com/bits_and_pieces/svg/samples/ -->
	  <div>
	    <span id="dec">
	      <button id="decrementOffset"> <-= </button>
						</span>
	    <span id="inc">
	      <button id="incrementOffset"> =-> </button>
	    </span>
	  </div>
	  <label id="CurrentRecordsDisplayed"></label>
	Reverse order button to sort by asc or desc date.
      </div>


    </div> <!-- SheriffSales -->

    <div id="RealEstateSales">
      <table>
	<tr>
	  <td>

	    <form name='myForm'>
	      Sale Amount between $<input type='text' id='minsale' value='1,000' />  and
	      $<input type='text' id='maxsale' value='2,000,000' />

	      <br>
	      Sale Validity:<select id='salevalidity'>
		<option value="*" selected>All</option>
		<option value='1'>Valid Sale</option>
		<option value='2'>Not Validated</option>
		<option value='3'>Related Individual or Corporations</option>
		<option value='4'>Liquidation or Foreclosure</option>
		<option value='5'>Not Open Market</option>
		<option value='6'>Partial Interest</option>
		<option value='7'>Land Contract or Unusual financing</option>
		<option value='8'>Excess personal pp or not arms length</option>
		<option value='9'>Owner Dishonesty in Description</option>
		<option value='10'>Sale involving multiple parcels</option>
	      </select>

	      Sale Type:<select id='saletype'>
		<option value="*" selected>All</option>
		<option value='1'>Land and Building</option>
		<option value='2'>Land Only</option>

	      </select>

	      Sale Date between<input type='text' id='startdate' value='2014-01-01' />  and
	      <input type='text' id='enddate' value='2014-04-23' />

	      <input type='button' onclick='Mapfunction("RealEstateSales",true)' value='Update Map' />

	    </form>
	  </td><td>
	    <!-- 	    <img src="Legend.gif" ALIGN=BOTTOM> -->
	  <div id="select-row">
	    <label> Number of Records To Display:</label>
	    <select onchange="Mapfunction('RealEstateSales',true)" id="recordstodisplay">
	      <option>10</option>
	      <option selected>25</option>
	      <option>50</option>
	      <option>75</option>
	      <option>100</option>
	      <option>150</option>
	      <option>200</option>
	      <option>250</option>
	      <option>500</option>
	      <option value='*'>All</option>
	    </select>
	  </div>

	  </td>
	</tr>
      </table>
    </div> <!-- end RealEstateSales div -->
    <div id="RentalRegistration">
      <div id="Menu">
	<div id="select-column">

            <label>District:</label>
            <select onchange="Mapfunction('RentalRegistration',true)" id='districtname'>
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
	      	 $sql="select distinct(DISTRICT_NAME) from RentalRegistrationMontgomeryCountyOhio order by DISTRICT_NAME asc"; //
	      	 //             echo $sql;
	      	 $rs=mysql_query($sql);
	      	 while($row = mysql_fetch_array($rs))
	      	 {
	      	 echo "<option value=\"".$row['DISTRICT_NAME']."\">".$row['DISTRICT_NAME']."</option>\n  ";
	      	 }
	      	 ?>

            </select>

            <label>Units:</label>
            <select onchange="Mapfunction('RentalRegistration',true)" id='numberofunits'>
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
	      	 $sql="select distinct(NUMBER_OF_UNITS) from RentalRegistrationMontgomeryCountyOhio order by NUMBER_OF_UNITS asc"; //
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
	    <select onchange="Mapfunction('RentalRegistration',true)" id="recordstodisplay">
	      <option>10</option>
	      <option selected>25</option>
	      <option>50</option>
	      <option>75</option>
	      <option>100</option>
	      <option>150</option>
	      <option>200</option>
	      <option>250</option>
	      <option>500</option>
	      <option value='*'>All</option>
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
    </div>  <!-- end RentalRegistration -->
    <div id="map" style="width: 100%; height: 85%"></div>
    <a href="mailto:maps@djinnius.com"> Questions?, comments</a>
    <script>
      $( "#radio1" ).click( function() 
      { 
      $("#SheriffSales").css("display","inline"); 
      $("#RealEstateSales").css("display","none");
      $("#RentalRegistration").css("display","none");
      Mapfunction("SheriffSales",false); //this will be the initial call so use 'false'
      });

      $( "#radio2" ).click( function() 
      { 
      $("#SheriffSales").css("display","none"); 
      $("#RealEstateSales").css("display","inline");
      $("#RentalRegistration").css("display","none");
      Mapfunction("RealEstateSales",false);
      });

      $( "#radio3" ).click( function() 
      { 
      $("#SheriffSales").css("display","none"); 
      $("#RealEstateSales").css("display","none");
      $("#RentalRegistration").css("display","inline");
      Mapfunction("RentalRegistration",false);
      });
    </script>
  </body>
</html>

