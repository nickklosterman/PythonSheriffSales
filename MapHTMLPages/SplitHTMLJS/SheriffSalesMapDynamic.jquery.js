var offset, recordstodisplay, curr_record =0;

$(document).ready(function(){




		      $("#incrementOffset").click(function(){
						      getRecordsValues();
						      curr_record += offset + recordstodisplay;
if (curr_record > recordCount)
{
curr_record = recordCount;
$("#inc").hide();
}

//						      alert(curr_record ); //, " ", offset, recordstodisplay);
						      writeout();
						      writeValuesToFormVariables();
						      $("#dec").show();
						      updateMap( );
						  });

		      $("#decrementOffset").click(function(){
						      getRecordsValues();
						      curr_record -= (offset + recordstodisplay) ; 
						      writeout();
						      writeValuesToFormVariables();
//						      alert(curr_record);
						      if ( curr_record < 0.1 )
						      {
							  curr_record = 0 ;
							  alert("too low");
							  $("#dec").hide();
						      }
$("#inc").show();
						      updateMap();
						  });

		  });

function writeout(){
    var rangelo = (curr_record+1);
    var rangehi = (curr_record+recordstodisplay);
    $("#currentrecord").html( rangelo.toString()+"-"+rangehi.toString()); //curr_record);
};

function writeValuesToFormVariables(){
    getRecordsValues();
    //set the form values (since we change it outside the form)
    document.myForm._recordstodisplay.value = recordstodisplay ;
    document.myForm._recordsoffset.value = curr_record ;//offset;


};

function getRecordsValues(){
    offset = parseInt(document.getElementById('recordsoffset').value); //wo the parseInt wrapper the value is interpreted as text
    //    alert(offset);
    recordstodisplay = parseInt(document.getElementById('recordstodisplay').value);
    //  alert(recordstodisplay);

};
