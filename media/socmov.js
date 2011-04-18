function show_flash_msg(txt) {
	$('#flash_notice').text( txt );
}
$(document).ready(function(){
	$("a[rel='backdrops']").colorbox({transition:"fade", width : "60%" , height:"60%"});
	$("a[rel='covers']").colorbox({slideshow:true });
	$(".video").colorbox({iframe:true, innerWidth:425, innerHeight:344});

	$(".vote_ui").click(function(){ 
		var elem = $(this);
		var movieid = elem.attr('movieid');
		var type = elem.hasClass('vote_up');
		
		$.ajax({
			url : "vote",
			data : { 'movieid' 	: movieid,
					 'type'		: type,
				   },
		}).success(
			function(data) {
				show_flash_msg("Successfully voted " + (type ? "up" : "down"));
				console.log("Successfully voted " + (type ? "up" : "down") );
			}
		).error(
			function (data) {
				show_flash_msg("Something went wrong");
				console.log("Something went wrong");
				console.log(data);
			}
		);
		return false;
	});

});

