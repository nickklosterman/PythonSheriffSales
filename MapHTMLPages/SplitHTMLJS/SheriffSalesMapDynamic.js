//need space between , and the next variable declaration. 
"use strict";
var markersArr = [];
var map;
var infoWindow;
var recordCount = 0;
var firstRun = true;

var customIcons = {
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




function clearLocations() {
    console.log("firstRun b:", firstRun);
    if (firstRun === false) {
        var i;
        infoWindow.close();
        for (i = 0; i < markersArr.length; i++) {
            markersArr[i].setMap(null);
        }
        markersArr.length = 0;
    } else {
        firstRun = false;
    }
    console.log("firstRun e:", firstRun);
}



function bindInfoWindow(marker, map, infoWindow, html) {
    google.maps.event.addListener(marker, 'click', function () {
        infoWindow.setContent(html);
        infoWindow.open(map, marker);
    });
}

function downloadUrl(url, callback) {
    var request;
    request = window.ActiveXObject ? new ActiveXObject('Microsoft.XMLHTTP') : new XMLHttpRequest;

    request.onreadystatechange = function () {
        if (request.readyState == 4) {
            //            request.onreadystatechange = doNothing;
            callback(request, request.status);
        }
    };

    request.open('GET', url, true);
    request.send(null);
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
    queryString = "http://djinnius.com/SheriffSales/Sandbox/phpdatabasequery.php?maxbid=2000000&minbid=1000&salestatus=*&saledate=*&pricefiltercategory=MinBid&table=Property&recordsoffset=0&recordstodisplay=205"; //must have spaces in btw + "" otherwise you break it!"; //must have spaces in btw + "" otherwise you break it!
    console.log("this query isn't pulling the variables from the inputs, its just hardcoded. this is one reason I wanna use updateMap() solely");
    console.log("load:", queryString);

    getRecordCountOfQuery(queryString);
    //    getRecordCountOfQuery(queryString);

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


    getRecordsValues();
    writeout();
    //need to check here so that can switch the values around in the html
    checkMinMaxBidValues(); //kinda overkill since check in the php as well. forgetting the damn ; at the end has screwed me several times.
    console.log("offset:", offset);
    recordsoffset = offset;
    queryString = "http://djinnius.com/SheriffSales/Sandbox/phpdatabasequery.php?maxbid=" + maxbid + "&minbid=" + minbid + "&salestatus=" + salestatus + "&saledate=" + saledate + "&pricefiltercategory=" + pricefiltercategory + "&table=Property&recordsoffset=" + recordsoffset + "&recordstodisplay=" + recordstodisplay; //must have spaces in btw + "" otherwise you break it!

    getRecordCountOfQuery(queryString);

    console.log("updatemap:", queryString);

    downloadUrl(queryString, function (data) {
        xml = data.responseXML;
        markers = xml.documentElement.getElementsByTagName("marker");
        if (firstRun !== true) {


            clearLocations(); // if I could figure out how to 

            //		     markersArr= new Array();
        } else {

            console.log("firstRun :", firstRun);
        }
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
    firstRun = false;
}


function getRecordCountOfQuery(oldQueryString) {
    var xml, record;
    var queryString = oldQueryString.replace(/phpdatabasequery/g, "phpgetrecordcount")
    console.log("getRecordCountOfQuery:", queryString);
    console.log("why doesn't it enter downloadUrl now?? I'm guessing that there is some sort of latency for downloadUrl to complete such that other functions are completed as we wait for downloadUrl to complete.");
    downloadUrl(queryString, function (data) {
        console.log("inside downloadUrl, is it just a delayed completion??");
        xml = data.responseXML;
        record = xml.documentElement.getElementsByTagName("data");
        console.log("record", record);
        recordCount = record[0].getAttribute("recordCount");
        console.log("recordCount in downloadUrl:", recordCount);
        writeout();
    });
    //    console.log("from what I can debug, it's a problem with the JS and not php as the php returns a valid xml item with a value. I do need to look into the diff btw what the mydql workbench is returning and the +1 value php is returning. I think it is because I'm using <= and >=. Yeah that appears to be it.")
    console.log("recordCount at exit:", recordCount);
}