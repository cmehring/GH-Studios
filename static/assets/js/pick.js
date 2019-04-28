$( ".far" ).click(function() {
	if ($(this).parent().get( 0 ).className.includes("like")) {
    $(this).parent().parent().removeClass("bad");
  } else {
  	$(this).parent().parent().toggleClass("bad")
  }

});