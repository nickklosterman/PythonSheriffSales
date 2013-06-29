//need space between , and the next variable declaration. 
"use strict";
var markersArr = [];
var map;
var infoWindow;
var recordCount = 0;

var customIcons = {
    1: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_green.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    2: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_black.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    NOBIDNOSALE: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_blue.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    },
    8: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_red.png',
        shadow: 'http://labs.google.com/ridefinder/images/mm_20_shadow.png'
    }
};

function clearLocations() {
        var i;
        infoWindow.close();
        for (i = 0; i < markersArr.length; i++) {
            markersArr[i].setMap(null);
        }
        markersArr.length = 0;
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
            callback(request, request.status);
        }
    };

    request.open('GET', url, true);
    request.send(null);
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
    queryString = "http://djinnius.com/SheriffSales/Sandbox/phpRentalRegistration.php?table=RentalRegistrationMontgomeryCountyOhio2013&recordsoffset=0&recordstodisplay=25";
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

function updateMap() {
    console.log("updateMap()");
    var  Parcel,Location,NumberOfUnits,  queryString, xml, markers, i, point, info, icon, marker;
    var pricefiltercategory, recordsoffset, recordstodisplay
    recordstodisplay = document.getElementById('recordstodisplay').value;
    writeout();
    recordsoffset = offset;
    queryString = "http://djinnius.com/SheriffSales/Sandbox/phpRentalRegistration.php?table=RentalRegistrationMontgomeryCountyOhio2013&recordsoffset=" + recordsoffset + "&recordstodisplay=" + recordstodisplay; //must have spaces in btw + "" otherwise you break it!
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


function getRecordCountOfQuery(oldQueryString) {
    var xml, record;
    var queryString = oldQueryString.replace(/phpRentalRegistration/g, "phpgetrecordcountRentalRegistration")
    downloadUrl(queryString, function (data) {
        console.log("inside downloadUrl, is it just a delayed completion??");
        xml = data.responseXML;
        record = xml.documentElement.getElementsByTagName("data");
        recordCount = record[0].getAttribute("recordCount");
        writeout();
    });

}
