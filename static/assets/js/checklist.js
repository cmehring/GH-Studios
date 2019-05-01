$("li").click(function() {
	 $(this).toggleClass("checked");
	 if ($(this).parent().children().length == $(this).parent().children(".checked").length) { // all are checked
		$(this).parent().parent()[0].children[0].src = "/static/assets/img/Platter Closed.png";
		$(this).parent().parent()[0].children[1].style.visibility = "hidden";
	 } else {
		$(this).parent().parent()[0].children[0].src = "/static/assets/img/Platter Open.png";
		$(this).parent().parent()[0].children[1].style.visibility = "visible";
	 }
});
