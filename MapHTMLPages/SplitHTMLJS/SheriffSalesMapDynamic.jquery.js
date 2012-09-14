var offset=0, recordstodisplay, curr_record =0;

$(document).ready(function(){
		      load();
//		      $("#dec").hide(); //initially we want to not allow the user to
 		      $("#incrementOffset").click(function(){
						      getRecordsValues();
						      curr_record +=  recordstodisplay;
						      console.log("curr_record:",curr_record,"recordCount:",recordCount);
						      if (curr_record+recordstodisplay > recordCount)
						      {
							  curr_record = recordCount-recordstodisplay;
							  //$("#inc").hide();
						      }

						      writeout();
						      
						      $("#dec").show();
						      updateMap( );
						      offset = curr_record ;
						  });
		      
		      $("#decrementOffset").click(function(){
						      getRecordsValues();
						      curr_record -= (recordstodisplay) ; 
						      writeout();
						      
						      if ( curr_record-recordstodisplay < 0.1 )
						      {
							  curr_record = 0 ;
							  console.log("too low");
							 // $("#dec").hide();
						      }
						      $("#inc").show();
						      updateMap();
						      offset = curr_record ;
						  });
		  });

function writeout(){
    var rangelo = (curr_record+1);
    var rangehi = (curr_record+recordstodisplay);
    $("#CurrentRecordsDisplayed").val( rangelo.toString()+"-"+rangehi.toString()); 
};

function getRecordsValues(){
    recordstodisplay = parseInt(document.getElementById('recordstodisplay').value);
    console.log("offset:",offset,"recordstodisplay:",recordstodisplay);
};

