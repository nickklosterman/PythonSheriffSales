
//keeping track of the input fields seems perfect for mvvm binding.
//is there a way we could just hover over the markers and have the data displayed? Or we could change the color of it and have the text displayed in a div on the side showing the relevant details.

"use strict";
var markersArr = [];
var map;
var infoWindow;

var recordCount = 0;
var firstRun = true;


var customIcons1 = {
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
var SheriffSaleStatusIcons = {
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

var RentalRegistrationNumberOfUnitsIcons = {
    1: {
        icon: 'http://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=|5600FC|000000&.png%3f', 
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

function getQueryString(database,isUpdate){ 
    var queryString, recordstodisplay; 
    if (isUpdate === false) {
	switch(database) {
	case "RealEstateSales":
//	    queryString = "http://www.djinnius.com/SheriffSales/Sandbox/SplitHTMLJS/Unified.php?maxbid=1000000000&minbid=1&saletype=*&salevalidity=*&startdate=2014-01-01&enddate=2014-09-09&table=RealEstateSalesMontgomeryCountyOhio&recordstodisplay=25";  //this query works
	    //relative urls get around the XSS blocking imposed by browsers.
	    queryString = "Unified.php?maxbid=1000000000&minbid=1&saletype=*&salevalidity=*&startdate=2014-01-01&enddate=2014-09-09&table=RealEstateSalesMontgomeryCountyOhio&recordstodisplay=25";  
	    break;
	case "RentalRegistration":
//	    queryString = "http://www.djinnius.com/SheriffSales/Sandbox/SplitHTMLJS/Unified.php?table=RentalRegistrationMontgomeryCountyOhio&recordsoffset=0&recordstodisplay=25&districtname=*&numberofunits=*";
	    queryString = "Unified.php?table=RentalRegistrationMontgomeryCountyOhio&recordsoffset=0&recordstodisplay=25&districtname=*&numberofunits=*";
	    break;
	case "SheriffSales":
//	    queryString = "http://www.djinnius.com/SheriffSales/Sandbox/SplitHTMLJS/Unified.php?maxbid=2000000&minbid=1000&salestatus=*&saledate=*&pricefiltercategory=MinBid&table=SheriffSalesMontgomeryCountyOhio&recordsoffset=0&recordstodisplay=25"; //must have spaces in btw + "" otherwise you break it!"; //must have spaces in btw + "" otherwise you break it!
	    queryString = "Unified.php?maxbid=2000000&minbid=1000&salestatus=*&saledate=*&pricefiltercategory=MinBid&table=SheriffSalesMontgomeryCountyOhio&recordsoffset=0&recordstodisplay=25"; //must have spaces in btw + "" otherwise you break it!"; //must have spaces in btw + "" otherwise you break it!
	    break;
	}
    } else { 

	var maxbid, minbid, saletype,salevalidity, startdate,enddate;
	var numberofunits,districtname;
	var salestatus , saledate,   pricefiltercategory ;
	
	switch(database) {
	case "RealEstateSales":
	    maxbid = $("#RealEstateSales #maxsale").val();
	    minbid = $("#RealEstateSales #minsale").val();
	    saletype = $("#RealEstateSales #saletype").val();
	    salevalidity = $("#RealEstateSales #salevalidity").val();
	    startdate = $("#RealEstateSales #startdate").val();
	    enddate = $("#RealEstateSales #enddate").val(); 

	    checkMinMaxBidValues(); 
//	    queryString = "http://www.djinnius.com/SheriffSales/Sandbox/SplitHTMLJS/Unified.php?maxbid=" + maxbid + "&minbid=" + minbid + "&salevalidity=" + salevalidity + "&saletype=" + saletype + "&startdate=" + startdate + "&enddate=" + enddate + "&table=RealEstateSalesMontgomeryCountyOhio"; //must have spaces in btw + "" otherwise you break it!
	    queryString = "Unified.php?maxbid=" + maxbid + "&minbid=" + minbid + "&salevalidity=" + salevalidity + "&saletype=" + saletype + "&startdate=" + startdate + "&enddate=" + enddate + "&table=RealEstateSalesMontgomeryCountyOhio"; //must have spaces in btw + "" otherwise you break it!
	    break;
	case "RentalRegistration":
	recordstodisplay = $("#RentalRegistration #recordstodisplay").val();
	    //console.log(recordstodisplay);
	    numberofunits = $("#RentalRegistration #numberofunits").val();
	    districtname = $("#RentalRegistration #districtname").val();
//	    queryString = "http://www.djinnius.com/SheriffSales/Sandbox/SplitHTMLJS/Unified.php?table=RentalRegistrationMontgomeryCountyOhio&recordsoffset=" + offset + "&recordstodisplay=" + recordstodisplay + "&districtname=" + districtname + "&numberofunits=" + numberofunits; //must have spaces in btw + "" otherwise you break it!
	    queryString = "Unified.php?table=RentalRegistrationMontgomeryCountyOhio&recordsoffset=" + offset + "&recordstodisplay=" + recordstodisplay + "&districtname=" + districtname + "&numberofunits=" + numberofunits; //must have spaces in btw + "" otherwise you break it!
	    //console.log(queryString);
	    break;
	case "SheriffSales":
	    recordstodisplay = $("#SheriffSales #recordstodisplay").val();
	    maxbid = $("#SheriffSales #maxbid").val();
	    minbid = $("#SheriffSales #minbid").val();
	    salestatus = $("#SheriffSales #salestatus").val();
	    saledate = $("#SheriffSales #saledate").val();
	    pricefiltercategory = $("#SheriffSales #pricefiltercategory").val();
	    checkMinMaxBidValues(); 
//	    queryString = "http://www.djinnius.com/SheriffSales/Sandbox/SplitHTMLJS/Unified.php?table=SheriffSalesMontgomeryCountyOhio&recordsoffset=" + offset + "&maxbid=" + maxbid + "&minbid=" + minbid + "&salestatus=" + salestatus + "&saledate=" + saledate + "&pricefiltercategory=" + pricefiltercategory + "&recordstodisplay=" + recordstodisplay; 
	    queryString = "Unified.php?table=SheriffSalesMontgomeryCountyOhio&recordsoffset=" + offset + "&maxbid=" + maxbid + "&minbid=" + minbid + "&salestatus=" + salestatus + "&saledate=" + saledate + "&pricefiltercategory=" + pricefiltercategory + "&recordstodisplay=" + recordstodisplay; 
	    break;
	}
    }

    return queryString
}

function Mapfunction(database,isUpdate){
    //console.log(database,isUpdate);
    var maxbid 
    , queryString;


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
    
    
    if (typeof map === 'undefined') // i.e. we are initializing the page
    {
	map = new google.maps.Map(document.getElementById("map"), {
            center: new google.maps.LatLng(39.7620028,-84.3542049), //center around Dayton, OH, USA
            zoom: 10,
            mapTypeId: 'roadmap'
	});
	infoWindow = new google.maps.InfoWindow;

    }
    queryString=getQueryString(database,isUpdate);
    getRecordCountOfQuery(queryString);
    downloadUrl( queryString, function(data) {
	processMarkers(database,data);
    });
}

function processMarkers(database,data) {
    var SaleDate ,
    PID ,
    SalePrice ,
    SaleType ,
    SaleValidity ,
    SaleTypenum ,
    SaleValiditynum ,
    SalePricenum ,
    CaseNumber ,
    Address ,
    ZipCode ,
    Plaintiff ,
    Defendant ,
    Attorney ,
    SoldTo ,
    Parcel , 
    NumberOfUnits , 
    PID ,
    Appraisal ,
    MinBid ,
    SaleAmt ,
    SaleStatus ,
    point ,
    info ,
    icon ,
    iconC ,
    marker ;

    //console.log(data);
    var xml = data.responseXML;// responseXML will be null but responseText and response will be populated if the returned result isn't xml
    //console.log("xml"+xml);
    if (xml !== null) {
        var markers = xml.documentElement.getElementsByTagName("marker");
	clearLocations();
	//console.log("processing Markers:"+database)
	switch(database){
	case "SheriffSales":
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
		    //console.log(document.getElementById("infowindow").value)
		}

		icon = SheriffSaleStatusIcons[SaleStatus] || {};
		marker = new google.maps.Marker({
		    map: map,
		    position: point,
		    icon: icon.icon,
		    shadow: icon.shadow
		});
		bindInfoWindow(marker, map, infoWindow, info);
		markersArr.push(marker);
	    }

	    break;
	case "RentalRegistration":
	    for (i = 0; i < markers.length; i++) {
		 Parcel = markers[i].getAttribute("Parcel");
		 Location = markers[i].getAttribute("Location");
		 NumberOfUnits = markers[i].getAttribute("NumberOfUnits");
		 point = new google.maps.LatLng(
		    parseFloat(markers[i].getAttribute("Latitude")),
		    parseFloat(markers[i].getAttribute("Longitude")));
		 info = "Parcel:" + Parcel + "<br/>Location:" + Location + "</br>Number Of Units:" + NumberOfUnits;
		 icon = RentalRegistrationNumberOfUnitsIcons[NumberOfUnits] || {};
		 marker = new google.maps.Marker({
		    map: map,
		    position: point,
		    icon: icon.icon,
		    shadow: icon.shadow
		});
		bindInfoWindow(marker, map, infoWindow, info);
		markersArr.push(marker);
	    }

	    break;
	case "RealEstateSales": 
            for (var i = 0; i < markers.length; i++) {
		 SaleDate = markers[i].getAttribute("SALEDT");
		 Address = markers[i].getAttribute("PARCELLOCATION");
		 PID = markers[i].getAttribute("PARID");
		 SalePrice = markers[i].getAttribute("PRICE");
		 SaleType = markers[i].getAttribute("SALETYPE");
		 SaleValidity = markers[i].getAttribute("SALEVALIDITY");
		 SaleTypenum = markers[i].getAttribute("SALETYPEnum");
		 SaleValiditynum = markers[i].getAttribute("SALEVALIDITYnum");
		 SalePricenum = markers[i].getAttribute("PRICEnum");

		 point = new google.maps.LatLng(
		    parseFloat(markers[i].getAttribute("Latitude")),
		    parseFloat(markers[i].getAttribute("Longitude"))
		);
		 info = "<b>Sale Date:" + SaleDate + "<br/>Address:" + Address + "<br/>Sale Amount:" + SalePrice + "</b> <br/>Sale Date:" + SaleDate +  "<br/>Address:"+ Address + "<br/>Parcel ID:" + PID + "<br/>Sale Price:" + SalePrice + "<br/>Sale Type:" + SaleType + "<br/> Sale Validity:" + SaleValidity;
		 iconC = IconCreator(SalePricenum);//,33,56);
		 marker = new google.maps.Marker({
		    map: map,
		    position: point,
		    icon: iconC,
		});
		bindInfoWindow(marker, map, infoWindow, info);
		markersArr.push(marker);
            }
	    break;
	} // switch 
    }// if (xml ...
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
    var thousands=Math.floor(price/divisor)-offset; // non-integer values break the color 
    if (thousands<0) {thousands=0}
    if (thousands>half) {
        if (thousands>509) {
            var color="ff0000"    ;
        } else {
            thousands=255-(thousands-255);
            color="ff00"+zeropad(thousands.toString(16));
        }
    } else {
        color=zeropad(thousands.toString(16))+"00ff";
    }
    return color;
}

function IconCreator(text)
{
    var modifiedtext = (text/1000)|0; //need to remove anything after a period
    var bgcolor = colormapper(text);
    var iconname = 'http://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=' + modifiedtext + '|' + bgcolor + '|000000&.png%3f';
    return iconname;
}

function clearLocations() {
    infoWindow.close();
    for (var i = 0; i < markersArr.length; i++) {
	markersArr[i].setMap(null);
    }
    markersArr.length = 0;
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

    if (parseInt(Minbid) > parseInt(Maxbid)) 
    {
        $("#maxbid")
            .value = Minbid;
        $("#minbid")
            .value = Maxbid;
    }
}

function getRecordCountOfQuery(oldQueryString) {
    var xml, record;
// The query is the same but we use a different php file to get the data. Therefore we simply replace the filename in the query
    var queryString = oldQueryString.replace(/Unified/g, "phpgetrecordcount") 
//    console.log(queryString);
    downloadUrl(queryString, function (data) {
	xml = data.responseXML;
	if (typeof xml !== 'undefined' && xml !== null ) {
            record = xml.documentElement.getElementsByTagName("data");
	    // console.log("record", record);
            recordCount = record[0].getAttribute("recordCount");
	    // console.log("recordCount in downloadUrl:", recordCount);
            writeout();
	}
    });
}
