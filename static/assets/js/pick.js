$( ".far" ).click(function() {
	if ($(this).parent().get( 0 ).className.includes("like")) {
    $(this).parent().parent().removeClass("bad");
	updateForm();
  } else {
  	$(this).parent().parent().toggleClass("bad")
	updateForm() ;
  }

});

function updateForm() {
	var listOf = [];
	for (var i = 0; i < document.getElementsByClassName("bad").length; i++) {
		listOf.push(document.getElementsByClassName("bad")[i].children[1].innerText);
	}	
	document.getElementById('listvalues').value = listOf;
}