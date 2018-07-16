$(document).ready(function() {

	$('.learn-more-btn').click(function() {

		var link = $(this).attr('href');

		$('html, body').animate({
			scrollTop: $(link).offset().top}, 600);
		return false;
	});

});
