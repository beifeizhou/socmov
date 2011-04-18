$(document).ready(function(){
	$("a[rel='backdrops']").colorbox({transition:"fade", width : "60%" , height:"60%"});
	$("a[rel='covers']").colorbox({slideshow:true });
	$(".video").colorbox({iframe:true, innerWidth:425, innerHeight:344});
});

$("#click").click(function(){ 
	$('#click')	.css({"background-color":"#f00", "color":"#fff", "cursor":"inherit"})
				.text("Open this window again and this message will still be here.");
				return false;
	});
