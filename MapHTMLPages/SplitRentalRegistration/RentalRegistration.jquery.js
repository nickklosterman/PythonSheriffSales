var offset = 0,
    recordstodisplay, curr_record = 0;

$(document).ready(function () {
    load();
    $("#incrementOffset").click(function () {
        console.log("--------------------------------INC------------------------");
        getRecordsValues();
        temp_curr_record=curr_record;
        curr_record += recordstodisplay;
        changeflag = false;
        console.log("Inc curr_record:", curr_record, "recordCount:", recordCount);

        if (curr_record + recordstodisplay > recordCount) {
            console.log("what");
            changeflag = true;
            curr_record = recordCount - recordCount % recordstodisplay;
        }

        offset = curr_record;
        writeout();

//        if (curr_record + recordstodisplay < recordCount && !changeflag) {
if(curr_record!=temp_curr_record)
{
            updateMap();
        }
    });

    $("#decrementOffset").click(function () {
        console.log("--------------------------------DEC------------------------");
        //don't do anything if we try to decrement the records yet are all ready viewing the first record count.
        if (curr_record != 0) {
            updateMap();
        }
        getRecordsValues();
        curr_record -= (recordstodisplay);
        if (curr_record < 0) {
            curr_record = 0
        }
        offset = curr_record;
        console.log("Dec curr_record:", curr_record, "recordCount:", recordCount);
        writeout();
    });
    $("#maxbid").change(function () {
        updateMap();
    });

    $("#minbid").change(function () {
        updateMap();
    });
});

function writeout() {
    var rangelo = (curr_record + 1);
    recordstodisplay = parseInt(document.getElementById('recordstodisplay').value);
    var rangehi = (curr_record + recordstodisplay);
    if (rangehi > recordCount) {
        rangehi = recordCount;
    }
    if (recordCount > 0) {
        if (recordstodisplay < recordCount) {
            console.log("recordstodisplay:", recordstodisplay, " recordCount:", recordCount, " curr_record", curr_record);
            $("#CurrentRecordsDisplayed").html("Displaying " + rangelo.toString() + "-" + rangehi.toString() + " of " + recordCount + " matching records.");
        }

        else {
            console.log("recordstodisplay:", recordstodisplay, " recordCount:", recordCount);
            $("#CurrentRecordsDisplayed").html("Displaying all matching records.");
        }
    }
    else {
        //js-beautify breaks this next line
        $("#CurrentRecordsDisplayed").html("<h3 style=\"color: red \" >There are no records to display using your criteria.</h3>");
    }

    console.log("Displaying " + rangelo.toString() + "-" + rangehi.toString() + " of " + recordCount + " matching records.");
};

function getRecordsValues() {
    recordstodisplay = parseInt(document.getElementById('recordstodisplay').value);
    console.log("offset:", offset, "recordstodisplay:", recordstodisplay);
};
