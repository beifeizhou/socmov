
$(document).ready(function(){
	$("a[rel='backdrops']").colorbox({transition:"fade", width : "60%" , height:"60%"});
	$("a[rel='covers']").colorbox({slideshow:true });
	$(".video").colorbox({iframe:true, innerWidth:425, innerHeight:344});

	$(".vote_ui").click(function(){ 
		var elem = $(this);
		var movieid = elem.attr('movieid');
		var type = elem.hasClass('vote_up');
		
		$.ajax({
			url : "/vote",
			data : { 'movieid' 	: movieid,
					 'type'		: type,
				   },
		}).success(
			function(data) {
				var parent = elem.parent().parent();
				parent.children().remove();
				parent.text("Thanks, you're vote has been sent");
				console.log("Successfully voted " + (type ? "up" : "down") );
				
				var block = parent.parent().parent();
				block.addClass('greyBox');
			}
		).error(
			function (xhr, ajaxOptions, thrownError) {
				console.log("Something went wrong");
				if (xhr.status == 403) {
					console.log("user not logged in :-/");
				}
			}
		);
		return false;
	});
	$.ajax({
		url : "/update_user_movies"
	}).success(
		function (data) {
			console.log( data );
		}
	);
	
	$('#invFriends').click(function(){
	FB.ui({	method	: 'apprequests', 
			message	: 'Discover movies. Socially.', 
			data	: 'tracking information for the user'});
	});
});

