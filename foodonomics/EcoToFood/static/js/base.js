$( document ).ready(function() {
	$("#selectType").on("click",appendParameters);
});

function appendParameters(){
	var n = $("#selectType").val();
	 $('.checkbox').remove();
	 $('#finalSubmit').remove();

	 $("#attachToMe").append('<input type="hidden" name="type" value='+n+'>');
	if (n==1){
		$("#attachToMe").append( "<div class=\"checkbox\"><label><input type=\"checkbox\" name=\"checks[]\" value=\"4\" />Property Price</label></div>"+
				"<div class=\"checkbox\"><label><input type=\"checkbox\" name=\"checks[]\" value=\"6\" />Educational Institutes</label></div>"+
				"<div class=\"checkbox\"><label><input type=\"checkbox\" name=\"checks[]\" value=\"7\" />Investment Companies</label></div>" );
	}else if(n==2){
			$("#attachToMe").append( "<div class=\"checkbox\"><label><input type=\"checkbox\" name=\"checks[]\" value=\"1\" />Number of Restaurants in area</label></div>"+
			"<div class=\"checkbox\"><label><input type=\"checkbox\" name=\"checks[]\" value=\"3\" />Population Density</label></div>"+
			"<div class=\"checkbox\"><label><input type=\"checkbox\" name=\"checks[]\" value=\"4\" />Property Price</label></div>" );

	}else if(n==3){
			$("#attachToMe").append( "<div class=\"checkbox\"><label><input type=\"checkbox\" name=\"checks[]\" value=\"1\" />Number of Restaurants in area</label></div>"+
			"<div class=\"checkbox\"><label><input type=\"checkbox\" name=\"checks[]\" value=\"4\" />Property Price</label></div>"+
			"<div class=\"checkbox\"><label><input type=\"checkbox\" name=\"checks[]\" value=\"5\" />Student Population Density</label></div>" );
	}
	$("#attachToMe").append("<input id='finalSubmit' type='submit' value='submit' name='submit'  />");
};


