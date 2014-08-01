
//keeping track of the input fields seems perfect for mvvm binding.
//is there a way we could just hover over the markers and have the data displayed? Or we could change the color of it and have the text displayed in a div on the side showing the relevant details.

"use strict";
var markersArr = [];
var map;
var infoWindow;
var query, maxbid , minbid ,  saletype ,  salevalidity ,  startdate ,  enddate ;

var recordCount = 0;
var firstRun = true;


var customIcons = {
    1: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_green.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    2: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_yellow.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    4: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_blue.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    8: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_red.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    }
};
var customIcons1 = {
    ACTIVE: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_green.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    CANCELLED: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_black.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    NOBIDNOSALE: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_blue.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    SOLD: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_red.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    }
};

var customIcons2 = {
    1: {
        icon: 'http://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=250|5600FC|000000&.png%3f', // http://labs.google.com/ridefinder/images/mm_20_green.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    2: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_black.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    3: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_blue.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    4: {

        icon: 'http://maps.google.com/mapfiles/ms/icons/lightblue.png', 
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    5: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_orange.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    6: {
        icon: 'http://maps.google.com/mapfiles/ms/icons/pink.png', 
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    7: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_purple.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    8: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_yellow.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    9: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_blue.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    10: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_blue.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    11: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_blue.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    12: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_blue.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    13: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_blue.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    14: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_blue.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    15: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_blue.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    16: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_red.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    }
};


function init(){
 maxbid = $("#maxbid").val();
 minbid = $("#minbid").val();
 saletype = $("#saletype option:selected").val();
 salevalidity = $("#salevalidity option:selected").val(); //http://api.jquery.com/selected-selector/
 startdate = $("#startdate").val();
 enddate = $("#enddate").val();

query.maxbid=maxbid;
query.minbid=minbid;
query.saletype=saletype ;
query.salevalidity=salevalidity;
query.startdate=startdate;
query.stopdate=stopdate;

updateMap();
}

$("#maxbid").change(function () {
query.maxbid=$("#maxbid").val();


})

function updateMap(){
/*    var maxbid = $("#maxbid").val();
    var minbid = $("#minbid").val();
    var saletype = $("#saletype").value;
    var salevalidity = $("#salevalidity").value;
    var startdate = $("#startdate").val();
    var enddate = $("#enddate").val();*/
    checkMinMaxBidValues(); //kinda overkill since check in the php as well. forgetting the damn ; at the end has screwed me several times.
    /*
      debug steps:
      make sure the php is returning valid results
      make sure the database is updated to what the local one shows
      make sure all variables have been appropriately changed if you edited old code. the yellow highlighting makes this tricky and non obvious source of errors (php)
      make sure all variables have been appropriately changed if you edited old code. the yellow highlighting makes this tricky and non obvious source of errors (js)
      validate the update function with a static query that you know works and delivers good php
      if its' from copied code that is known good then it is most likely SPELLING SPELLING SPELLING of variables or files.

    */
    var queryString = "phpRealEstateSalesDynamic.php?maxbid=" + maxbid + "&minbid=" + minbid + "&salevalidity=" + salevalidity + "&saletype=" + saletype + "&startdate=" + startdate + "&enddate=" + enddate + "&table=RealEstateSalesMontgomeryCountyOhio"; //must have spaces in btw + "" otherwise you break it!

    //alert (queryString)
    //queryString = "phpRealEstateSalesDynamic.php?maxbid=100000&minbid=1&saletype=1&salevalidity=1&startdate=2013-03-01&enddate=2013-04-04&table=RealEstateSalesMontgomeryCountyOhio";  //this query works
    downloadUrl( queryString, function(data) {
        var xml = data.responseXML;
        markers = xml.documentElement.getElementsByTagName("marker");
	clearLocations();
        for (var i = 0; i < markers.length; i++) {
            var SaleDate = markers[i].getAttribute("SALEDT");
            var Address = markers[i].getAttribute("PARCELLOCATION");
            var PID = markers[i].getAttribute("PARID");
            var SalePrice = markers[i].getAttribute("PRICE");
            var SaleType = markers[i].getAttribute("SALETYPE");
            var SaleValidity = markers[i].getAttribute("SALEVALIDITY");
            var SaleTypenum = markers[i].getAttribute("SALETYPEnum");
            var SaleValiditynum = markers[i].getAttribute("SALEVALIDITYnum");


            var point = new google.maps.LatLng(
		parseFloat(markers[i].getAttribute("Latitude")),
		parseFloat(markers[i].getAttribute("Longitude"))
            );

	    var info = "<b>Sale Date:" + SaleDate + "<br/>Address:" + Address + "<br/>Sale Amount:" + SalePrice + "</b> <br/>Sale Date:" + SaleDate +  "<br/>Address:"+ Address + "<br/>Parcel ID:" + PID + "<br/>Sale Price:" + SalePrice + "<br/>Sale Type:" + SaleType + "<br/> Sale Validity:" + SaleValidity;

            var icon = customIcons[SaleValiditynum] || {};

            var marker = new google.maps.Marker({
		map: map,
		position: point,
		icon: icon.icon,
		shadow: icon.shadow
	    });
            bindInfoWindow(marker, map, infoWindow, info);
	    markersArr.push(marker);
        }
    });

}


function Mapfunction(database,isUpdate){
/*    var maxbid = $("#maxbid").val();
    var minbid = $("#minbid").val();
    var saletype = $("#saletype").value;
    var salevalidity = $("#salevalidity").val();
    var startdate = $("#startdate").val();
    var enddate = $("#enddate").val(); */
    //alert (maxbid,minbid,saletype,salevalidity,startdate,enddate)
switch(database){
case "SheriffSales":
    checkMinMaxBidValues(); 
break;
case "RealEstateSales": 
    checkMinMaxBidValues(); 
break;
}
    /*
      debug steps:
      make sure the php is returning valid results
      make sure the database is updated to what the local one shows
      make sure all variables have been appropriately changed if you edited old code. the yellow highlighting makes this tricky and non obvious source of errors (php)
      make sure all variables have been appropriately changed if you edited old code. the yellow highlighting makes this tricky and non obvious source of errors (js)
      validate the update function with a static query that you know works and delivers good php
      if its' from copied code that is known good then it is most likely SPELLING SPELLING SPELLING of variables or files.
      when assigning variables there must be a space between the operator and the names of variables: i.e. bob=88 fails but bob = 88 works

    */
    if (isUpdate === false)
    {
	map = new google.maps.Map(document.getElementById("map"), {
            center: new google.maps.LatLng(39.7620028,-84.3542049),
            zoom: 10,
            mapTypeId: 'roadmap'
	});
	infoWindow = new google.maps.InfoWindow;
	var queryString = "http://www.djinnius.com/SheriffSales/Sandbox/phpRealEstateSalesDynamic.php?maxbid=1000000000&minbid=1&saletype=*&salevalidity=*&startdate=2013-09-01&enddate=2013-09-09&table=RealEstateSalesMontgomeryCountyOhio";  //this query works
    }
    else
    {
	var queryString = "http://www.djinnius.com/SheriffSales/Sandbox/phpRealEstateSalesDynamic.php?maxbid=" + maxbid + "&minbid=" + minbid + "&salevalidity=" + salevalidity + "&saletype=" + saletype + "&startdate=" + startdate + "&enddate=" + enddate + "&table=RealEstateSalesMontgomeryCountyOhio"; //must have spaces in btw + "" otherwise you break it!
    }
    //alert (queryString)
    downloadUrl( queryString, function(data) {
        var xml = data.responseXML;
	if (xml !== null) {
        var markers = xml.documentElement.getElementsByTagName("marker");
	clearLocations();
        for (var i = 0; i < markers.length; i++) {
            var SaleDate = markers[i].getAttribute("SALEDT");
            var Address = markers[i].getAttribute("PARCELLOCATION");
            var PID = markers[i].getAttribute("PARID");
            var SalePrice = markers[i].getAttribute("PRICE");
            var SaleType = markers[i].getAttribute("SALETYPE");
            var SaleValidity = markers[i].getAttribute("SALEVALIDITY");
            var SaleTypenum = markers[i].getAttribute("SALETYPEnum");
            var SaleValiditynum = markers[i].getAttribute("SALEVALIDITYnum");
            var SalePricenum = markers[i].getAttribute("PRICEnum");

            var point = new google.maps.LatLng(
		parseFloat(markers[i].getAttribute("Latitude")),
		parseFloat(markers[i].getAttribute("Longitude"))
            );

	    var info = "<b>Sale Date:" + SaleDate + "<br/>Address:" + Address + "<br/>Sale Amount:" + SalePrice + "</b> <br/>Sale Date:" + SaleDate +  "<br/>Address:"+ Address + "<br/>Parcel ID:" + PID + "<br/>Sale Price:" + SalePrice + "<br/>Sale Type:" + SaleType + "<br/> Sale Validity:" + SaleValidity;

	    //           var icon = customIcons[SaleValiditynum] || {};
            var iconC = IconCreator(SalePricenum,33,56);

            var marker = new google.maps.Marker({
		map: map,
		position: point,
		//          icon: icon.icon,
		icon: iconC,
		//shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png' // we don't really want a shadow as it actually isn't placed correctly. it is  little to the left
		//            shadow: icon.shadow
		//        icon: 'http://labs.google.com/ridefinder/images/mm_20_green.png',  shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'

            });
            bindInfoWindow(marker, map, infoWindow, info);
	    markersArr.push(marker);
        }
	}
    });

}
function zeropad(number)
{
    if (number.length==1)
    {
        number="0"+number;
    }
    return number;

}

function colormapper(price)
{
    var div=1; //increase this value to make colors be more distinct over a shorter range. i.e. increaseing the value maps the colors to a narrower value range.
    var offset=5*div; //offset is the dollar offset in $1000s of dollars i.e. 41 ->$41,000 is bottom of color bar and 509+41->$550,000 is top (if div=1)
    var divisor=1000/div; //make the divisor smaller to make details pop out. 500 seems to work well.
    var half=255;
    var thousands=price/divisor-offset;
    if (thousands<0) {thousands=0}
    if (thousands>half)
    {
        if (thousands>509)
        {
           var color="ff0000"    ;
        }
        else{
            thousands=255-(thousands-255);
            color="ff00"+zeropad(thousands.toString(16));
        }
    }
    else
    {
        color=zeropad(thousands.toString(16))+"00ff";
    }
    return color;
}


/**/
function IconCreator(text,bgcolor,textcolor)
{
    //var RE = new RegExp("\$","");
    //var modifiedtext = RE.exec(text);
    var modifiedtext = (text/1000)|0; //need to ermove anything after a period
    var textcolor = "000000";
    //textcolor = "ffffff";
    var bgcolor = "56fffc";
    bgcolor = "00ff00";
    bgcolor = colormapper(text);
    //bgcolor = colormapper2(text);
    //var iconname = "http://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=" + modifiedtext + "-=-" + text + "|" + bgcolor + "|" + textcolor + "&.png%3f";
    var iconname = 'http://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=' + modifiedtext + '|' + bgcolor + '|' + textcolor + '&.png%3f';
    //alert(iconname);
    return iconname;
}
/**/



function clearLocations() {
    infoWindow.close();
    for (var i = 0; i < markersArr.length; i++) {
	markersArr[i].setMap(null);
    }
    markersArr.length = 0;
}



function load() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: new google.maps.LatLng(39.7620028,-84.3542049), //pass in the center and we can use the same map for PGH stuff as well.
        zoom: 10,
        mapTypeId: 'roadmap'
    });
    infoWindow = new google.maps.InfoWindow;
    alert("Make me one function and pass in 1 or 0 and based on that pass premade query or construct query")
    var queryString = "phpRealEstateSalesDynamic.php?maxbid=1000000000&minbid=1&saletype=*&salevalidity=*&startdate=2013-01-01&enddate=2013-04-04&table=RealEstateSalesMontgomeryCountyOhio";  //this query works
    downloadUrl(queryString, function(data) {
        var xml = data.responseXML;
        var markers = xml.documentElement.getElementsByTagName("marker");
        for (var i = 0; i < markers.length; i++) {
            var SaleDate = markers[i].getAttribute("SALEDT");
            var Address = markers[i].getAttribute("PARCELLOCATION");
            var PID = markers[i].getAttribute("PARID");
            var SalePrice = markers[i].getAttribute("PRICE");
            var SaleType = markers[i].getAttribute("SALETYPE");
            var SaleValidity = markers[i].getAttribute("SALEVALIDITY");
            var SaleTypenum = markers[i].getAttribute("SALETYPEnum");
            var SaleValiditynum = markers[i].getAttribute("SALEVALIDITYnum");

            var point = new google.maps.LatLng(
		parseFloat(markers[i].getAttribute("Latitude")),
		parseFloat(markers[i].getAttribute("Longitude")));

	    var info = "<b>Sale Date:" + SaleDate + "<br/>Address:" + Address + "<br/>Sale Amount:" + SalePrice + "</b> <br/>Sale Date:" + SaleDate +  "<br/>Address:"+ Address + "<br/>Parcel ID:" + PID + "<br/>Sale Price:" + SalePrice + "<br/>Sale Type:" + SaleType + "<br/> Sale Validity:" + SaleValidity;

            var icon = customIcons[SaleValiditynum] || {};          var icon = customIcons[3] || {};

            var marker = new google.maps.Marker({
		map: map,
		position: point,

		icon: icon.icon,
		shadow: icon.shadow
		//        icon: 'http://labs.google.com/ridefinder/images/mm_20_green.png',        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'

            });
            bindInfoWindow(marker, map, infoWindow, info);
	    markersArr.push(marker);

        }
    });
    /*
      doesn't this screw stuff up as I need == not =?
      if (myForm.infowindow.value="Summary") //Detailed")//"
      {
      alert("Detaileded");
      }
      else alert("Summarily");
    */
}

function bindInfoWindow(marker, map, infoWindow, html) {
    google.maps.event.addListener(marker, 'click', function() {
        infoWindow.setContent(html);
        infoWindow.open(map, marker);
    });
}

function downloadUrl(url, callback) {
    var request = window.ActiveXObject ?
        new ActiveXObject('Microsoft.XMLHTTP') :
        new XMLHttpRequest;

    request.onreadystatechange = function() {
        if (request.readyState == 4) {
            request.onreadystatechange = doNothing;
            callback(request, request.status);
        }
    };

    request.open('GET', url, true);
    request.send(null);
}

function doNothing() {}


function checkMinMaxBidValues()
{
    var Maxbid0=myForm.maxbid.value;
    var Maxbid=Maxbid0.replace(/,/g,"");
    var Minbid0=myForm.minbid.value;
    var Minbid=Minbid0.replace(/,/g,"");

    if (parseInt(Minbid) > parseInt(Maxbid)) //phail ! spaces in () statement
	if (parseInt(Minbid)>parseInt(Maxbid)) //Good. no spaces
    {
	myForm.maxbid.value=Minbid;
	//myForm.minbid.text.value=Maxbid; //doesn't work!!
	myForm.minbid.value=Maxbid;
    }

}
function checkMinMaxBidValues() {
    var Maxbid0, Maxbid, Minbid0, Minbid;

    Maxbid0 = document.getElementById('maxbid')
        .value;
    Minbid0 = document.getElementById('minbid')
        .value;

    Maxbid = Maxbid0.replace(/,/g, "");
    Minbid = Minbid0.replace(/,/g, "");

    if (parseInt(Minbid) > parseInt(Maxbid)) //phail ! spaces in () statement
    if (parseInt(Minbid) > parseInt(Maxbid)) //Good. no spaces
    {
        $("#maxbid")
            .value = Minbid;
        $("#minbid")
            .value = Maxbid;
    }


}





function updateMap() {
    console.log("updateMap()");
    var  Parcel,Location,NumberOfUnits,  queryString, xml, markers, i, point, info, icon, marker;
    var pricefiltercategory, recordsoffset, recordstodisplay
    recordstodisplay = document.getElementById('recordstodisplay').value;
    districtname = document.getElementById('districtname').value;
    numberofunits = document.getElementById('numberofunits').value;
    writeout();
    recordsoffset = offset;
    queryString = "http://djinnius.com/SheriffSales/Sandbox/phpRentalRegistration.php?table=RentalRegistrationMontgomeryCountyOhio2013&recordsoffset=" + recordsoffset + "&recordstodisplay=" + recordstodisplay + "&districtname=" + districtname + "&numberofunits=" + numberofunits; //must have spaces in btw + "" otherwise you break it!
    getRecordCountOfQuery(queryString);
    console.log("updatemap:", queryString);
    clearLocations();
    downloadUrl(queryString, function (data) {
        xml = data.responseXML;
        markers = xml.documentElement.getElementsByTagName("marker");
        for (i = 0; i < markers.length; i++) {
            Parcel = markers[i].getAttribute("Parcel");
            Location = markers[i].getAttribute("Location");
            NumberOfUnits = markers[i].getAttribute("NumberOfUnits");
            point = new google.maps.LatLng(
            parseFloat(markers[i].getAttribute("Latitude")),
            parseFloat(markers[i].getAttribute("Longitude")));
            info = "Parcel:" + Parcel + "<br/>Location:" + Location + "</br>Number Of Units:" + NumberOfUnits;
            icon = customIcons[NumberOfUnits] || {};
            marker = new google.maps.Marker({
                map: map,
                position: point,
                icon: icon.icon,
                shadow: icon.shadow
            });
            bindInfoWindow(marker, map, infoWindow, info);
            markersArr.push(marker);
        }
    });
}
function updateMap() {
    console.log("updateMap()");
    var maxbid, minbid, salestatus, saledate, queryString, xml, markers, i, SaleDate, CaseNumber, Address, ZipCode, Plaintiff, Defendant, Attorney, SoldTo, PID, Appraisal, MinBid, SaleAmt, SaleStatus, point, info, icon, marker;
    var pricefiltercategory, recordsoffset, recordstodisplay

    maxbid = document.getElementById('maxbid')
        .value;
    minbid = document.getElementById('minbid')
        .value;
    salestatus = document.getElementById('salestatus')
        .value;
    saledate = document.getElementById('saledate')
        .value;
    pricefiltercategory = document.getElementById('pricefiltercategory')
        .value;

    recordstodisplay = document.getElementById('recordstodisplay')
        .value;
    console.log("recordstodisplay:", recordstodisplay);
//    getRecordsValues(); //redundant
    writeout();
    //need to check here so that can switch the values around in the html
    checkMinMaxBidValues(); //kinda overkill since check in the php as well. forgetting the damn ; at the end has screwed me several times.
    console.log("offset:", offset);
    recordsoffset = offset;
//    queryString = "http://djinnius.com/SheriffSales/Sandbox/phpdatabasequery.php?maxbid=" + maxbid + "&minbid=" + minbid + "&salestatus=" + salestatus + "&saledate=" + saledate + "&pricefiltercategory=" + pricefiltercategory + "&table=Property&recordsoffset=" + recordsoffset + "&recordstodisplay=" + recordstodisplay; //must have spaces in btw + "" otherwise you break it!
    queryString = "../../php/phpdatabasequery.php?maxbid=" + maxbid + "&minbid=" + minbid + "&salestatus=" + salestatus + "&saledate=" + saledate + "&pricefiltercategory=" + pricefiltercategory + "&table=Property&recordsoffset=" + recordsoffset + "&recordstodisplay=" + recordstodisplay; //must have spaces in btw + "" otherwise you break it!

    getRecordCountOfQuery(queryString);

    console.log("updatemap:", queryString);
    clearLocations();
    downloadUrl(queryString, function (data) {
        xml = data.responseXML;
        markers = xml.documentElement.getElementsByTagName("marker");
        for (i = 0; i < markers.length; i++) {
            SaleDate = markers[i].getAttribute("SaleDate");
            CaseNumber = markers[i].getAttribute("CaseNumber");
            Address = markers[i].getAttribute("Address");
            ZipCode = markers[i].getAttribute("ZipCode");
            Plaintiff = markers[i].getAttribute("Plaintiff");
            Defendant = markers[i].getAttribute("Defendant");
            Attorney = markers[i].getAttribute("Attorney");
            SoldTo = markers[i].getAttribute("SoldTo");
            PID = markers[i].getAttribute("PID");
            Appraisal = markers[i].getAttribute("Appraisal");
            MinBid = markers[i].getAttribute("MinBid");
            SaleAmt = markers[i].getAttribute("SaleAmt");
            SaleStatus = markers[i].getAttribute("SaleStatus");


            point = new google.maps.LatLng(
            parseFloat(markers[i].getAttribute("Latitude")),
            parseFloat(markers[i].getAttribute("Longitude")));
            //if ($("#infowindow").value=="Detailed") //for some reason this method to access the value no longer works. Ahh cuz prev it was in a form and now its a input field.
            if (document.getElementById("infowindow")
                .value == "Detailed") {
                info = "<b>Sale Date:" + SaleDate + "<br/>Address:" + Address + "<br/>Sale Amount:" + SaleAmt + "</b> <br/>Sale Date:" + SaleDate + "<br/>Case Number:" + CaseNumber + "<br/>Address:" + Address + "<br/>Zipcode:" + ZipCode + "<br/>Plaintiff:" + Plaintiff + "<br/>Defendant:" + Defendant + "<br/>Attorney:" + Attorney + "<br/>Sold to:" + SoldTo + "<br/>Parcel ID:" + PID + "<br/>Appraisal:" + Appraisal + "<br/>Minimum bid:" + MinBid + "<br/>Sale amount:" + SaleAmt + "<br/> Sale status:" + SaleStatus;
            } else if (document.getElementById("infowindow")
                .value == "Summary") {
                info = "<b>Sale Date:" + SaleDate + "<br/>Address:" + Address + "<br/>Sale Amount:" + SaleAmt + "</b> <br/>Sale Date:" + SaleDate + "<br/>Appraisal:" + Appraisal + "<br/>Minimum bid:" + MinBid + "<br/>Sale amount:" + SaleAmt + "<br/> Sale status:" + SaleStatus;
            } else {
                console.log(document.getElementById("infowindow")
                    .value)
            }

            icon = customIcons[SaleStatus] || {};
            marker = new google.maps.Marker({
                map: map,
                position: point,
                icon: icon.icon,
                shadow: icon.shadow
            });
            bindInfoWindow(marker, map, infoWindow, info);
            markersArr.push(marker);
        }
    });

}

function getRecordCountOfQuery(oldQueryString) {
    var xml, record;
    var queryString = oldQueryString.replace(/phpdatabasequery/g, "phpgetrecordcount")

    downloadUrl(queryString, function (data) {
        xml = data.responseXML;
        record = xml.documentElement.getElementsByTagName("data");
//        console.log("record", record);
        recordCount = record[0].getAttribute("recordCount");
//        console.log("recordCount in downloadUrl:", recordCount);
        writeout();
    });
}


function load() {
    console.log("load()");
    var queryString, xml, markers,  Parcel,Location,NumberOfUnits, point, info, icon, marker;
    map = new google.maps.Map(document.getElementById("map"), {
        center: new google.maps.LatLng(39.7620028, - 84.3542049),
        zoom: 10,
        mapTypeId: 'roadmap'
    });
    infoWindow = new google.maps.InfoWindow;
    queryString = "http://djinnius.com/SheriffSales/Sandbox/phpRentalRegistration.php?table=RentalRegistrationMontgomeryCountyOhio2013&recordsoffset=0&recordstodisplay=25&districtname=*&numberofunits=*";
    getRecordCountOfQuery(queryString);
    console.log("updatemap:", queryString);
    downloadUrl(queryString, function (data) {
        xml = data.responseXML;
        markers = xml.documentElement.getElementsByTagName("marker");
        for (var i = 0; i < markers.length; i++) {
            Parcel = markers[i].getAttribute("Parcel");
            Location = markers[i].getAttribute("Location");
            NumberOfUnits = markers[i].getAttribute("NumberOfUnits");
            point = new google.maps.LatLng(
            parseFloat(markers[i].getAttribute("Latitude")),
            parseFloat(markers[i].getAttribute("Longitude")));
            info = "<br/>Parcel:" + Parcel + "<br/>Location:" + Location + "</br>Number Of Units" + NumberOfUnits;
            icon = customIcons[NumberOfUnits] || {};
            marker = new google.maps.Marker({
                map: map,
                position: point,
                icon: icon.icon,
                shadow: icon.shadow
            });
            bindInfoWindow(marker, map, infoWindow, info);
            markersArr.push(marker);
        }
    });
}


function load() {
    console.log("load()");
    var queryString, xml, markers, SaleDate, CaseNumber, Address, ZipCode, Plaintiff, Defendant, Attorney, SoldTo, PID, Appraisal, MinBid, SaleAmt, SaleStatus, point, info, icon, marker;
    map = new google.maps.Map(document.getElementById("map"), {
        center: new google.maps.LatLng(39.7620028, - 84.3542049),
        zoom: 10,
        mapTypeId: 'roadmap'
    });
    infoWindow = new google.maps.InfoWindow;

    //    queryString = "http://djinnius.com/SheriffSales/Sandbox/phpdatabasequery.php?maxbid=2000000&minbid=1000&salestatus=*&saledate=*&pricefiltercategory=Appraisal&table=Property&recordsoffset=0&recordstodisplay=50"; //must have spaces in btw + "" otherwise you break it!"; //must have spaces in btw + "" otherwise you break it!
//    queryString = "http://djinnius.com/SheriffSales/Sandbox/phpdatabasequery.php?maxbid=2000000&minbid=1000&salestatus=*&saledate=*&pricefiltercategory=MinBid&table=Property&recordsoffset=0&recordstodisplay=205"; //must have spaces in btw + "" otherwise you break it!"; //must have spaces in btw + "" otherwise you break it!
    queryString = "../../php/phpdatabasequery.php?maxbid=2000000&minbid=1000&salestatus=*&saledate=*&pricefiltercategory=MinBid&table=Property&recordsoffset=0&recordstodisplay=205"; //must have spaces in btw + "" otherwise you break it!"; //must have spaces in btw + "" otherwise you break it!
    console.log("this query isn't pulling the variables from the inputs, its just hardcoded. this is one reason I wanna use updateMap() solely");
    console.log("load:", queryString);

    getRecordCountOfQuery(queryString);

    downloadUrl(queryString, function (data) {
        xml = data.responseXML;
        markers = xml.documentElement.getElementsByTagName("marker");
        for (var i = 0; i < markers.length; i++) {
            SaleDate = markers[i].getAttribute("SaleDate");
            CaseNumber = markers[i].getAttribute("CaseNumber");
            Address = markers[i].getAttribute("Address");
            ZipCode = markers[i].getAttribute("ZipCode");
            Plaintiff = markers[i].getAttribute("Plaintiff");
            Defendant = markers[i].getAttribute("Defendant");
            Attorney = markers[i].getAttribute("Attorney");
            SoldTo = markers[i].getAttribute("SoldTo");
            PID = markers[i].getAttribute("PID");
            Appraisal = markers[i].getAttribute("Appraisal");
            MinBid = markers[i].getAttribute("MinBid");
            SaleAmt = markers[i].getAttribute("SaleAmt");
            SaleStatus = markers[i].getAttribute("SaleStatus");


            point = new google.maps.LatLng(
            parseFloat(markers[i].getAttribute("Latitude")),
            parseFloat(markers[i].getAttribute("Longitude")));

            info = "";
            //if ($("#infowindow").value=="Detailed") //for some reason this method to access the value no longer works. Ahh cuz prev it was in a form and now its a input field.
            if (document.getElementById("infowindow")
                .value == "Detailed") {
                info = "<b>Sale Date:" + SaleDate + "<br/>Address:" + Address + "<br/>Sale Amount:" + SaleAmt + "</b> <br/>Sale Date:" + SaleDate + "<br/>Case Number:" + CaseNumber + "<br/>Address:" + Address + "<br/>Zipcode:" + ZipCode + "<br/>Plaintiff:" + Plaintiff + "<br/>Defendant:" + Defendant + "<br/>Attorney:" + Attorney + "<br/>Sold to:" + SoldTo + "<br/>Parcel ID:" + PID + "<br/>Appraisal:" + Appraisal + "<br/>Minimum bid:" + MinBid + "<br/>Sale amount:" + SaleAmt + "<br/> Sale status:" + SaleStatus;
            } else if (document.getElementById("infowindow")
                .value == "Summary") {
                info = "<b>Sale Date:" + SaleDate + "<br/>Address:" + Address + "<br/>Sale Amount:" + SaleAmt + "</b> <br/>Sale Date:" + SaleDate + "<br/>Appraisal:" + Appraisal + "<br/>Minimum bid:" + MinBid + "<br/>Sale amount:" + SaleAmt + "<br/> Sale status:" + SaleStatus;
            } else {
                console.log(document.getElementById("infowindow")
                    .value)
            }

            icon = customIcons[SaleStatus] || {};

            marker = new google.maps.Marker({
                map: map,
                position: point,
                icon: icon.icon,
                shadow: icon.shadow
            });
            bindInfoWindow(marker, map, infoWindow, info);
            markersArr.push(marker);

        }
    });
    console.log("I would really like to figure out how to use clearLocations() without it barfing when markersArr isn't populated. That way I can get rid of load() and just use updateMap().");

}




