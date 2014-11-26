<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <title>Montgomery County Sheriff Sales</title>
    <link rel="stylesheet" type="text/css" href="SheriffSalesMapDynamic.css" />
    <script src="http://maps.google.com/maps/api/js?sensor=false" type="text/javascript"></script>
<!--    <script type="text/javascript" src="jquery-1.8.0.min.js"></script> -->
    <script type="text/javascript" src="http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.1/jquery.js"></script>
    <script src="SheriffSalesMapDynamic.js"></script>
    <script src="SheriffSalesMapDynamic.jquery.js"></script>
  </head>
  <body>
    <div id="Menu">
      <div id="select-column">
	<div id="select-row">
	  <select onchange="updateMap()" id='pricefiltercategory'>
	    <option value="MinBid">Minimum Bid</option>
	    <option value="Appraisal">Appraisal Amount</option>
	    <option value="SaleAmt">Sale Amount</option>
	  </select>
	  <!--
	      http://www.skytopia.com/project/articles/compsci/form.html how to dynamically execute according to which list/dropdown/radio is selected.
	      Minimum Bid
	    -->
	</div>
	<div id="select-row">
	  <label>between</label>
	  $<input type='text' id='minbid' value='1,000' />
	</div>
	<div id="select-row">
	  <label>and</label>
	  $<input type='text' id='maxbid' value='2,000,000' />
	</div>
      </div>

      <div id="select-column">
	<div id="select-row">
	  <label>Sale Status:</label>
	  <select onchange="updateMap()" id='salestatus'>
	    <option value="*" selected>All</option>
	    <option>Active</option>
	    <option>Sold</option>
	    <option>Cancelled</option>
	    <option>No Bid, No Sale</option>
	  </select>
	</div>
	<div id="select-row">
	  <label>Sale Date:</label>
	  <select onchange="updateMap()" id='saledate'>
	    <option value="*" selected>All</option>
        <?php
             //specifies username,password,database, and table
             //require("../dbinfo_user.php");
	     require("../php/dbinfo_local.php");
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
             $sql="select distinct(SaleDate) from Property where not zipcode=0 order by SaleDate desc"; //
//             echo $sql;
             $rs=mysql_query($sql);
             while($row = mysql_fetch_array($rs))
             {
             echo "<option value=\"".$row['SaleDate']."\">".$row['SaleDate']."</option>\n  ";
             //  echo '<option>'.$row['SaleDate'].'</option>\n';
             }
             ?>

	  </select>
	</div>
	<div id="select-row">
	  <label>Info Window:</label>
	  <select onchange="updateMap()" id='infowindow'>
	    <!--   onChange="updateMap3()"> -->
	    <option >Detailed</option>
	    <option >Summary</option>
	  </select>
	</div>
      </div>

      <div id="select-column">
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

	<!-- I could add an image here. there are multiple options now: css,svg,canvas
	     http://www.scriptol.com/html5/button.php
	     http://croczilla.com/bits_and_pieces/svg/samples/ -->

	<div id="select-row">
	  <div id="dec">
	    <button id="decrementOffset"> <-= </button>
					      </div>
	</div>
	<div id="select-row">
	  <div id="inc">
	    <button id="incrementOffset"> =-> </button>
	  </div>
	</div>
      </div>
      <div id="select-row">
	<!--      <input type='button' onClick='iterate()' > -->
	<label id="CurrentRecordsDisplayed"></label>
      </div>
      Reverse order button to sort by asc or desc date.
    </div>
    <!--	  <img src="Legend.gif" ALIGN=BOTTOM>  -->

    <div id="map" style="width: 100%; height: 85%"></div>
    <a href="mailto:maps@djinnius.com"> Questions?, comments</a>
  </body>
</html>
