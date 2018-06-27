$(document).ready(function() {

	$('.learn-more-btn').click(function() {

		var link = $(this).attr('href');

		$('html, body').animate({
			scrollTop: $(link).offset().top}, 600);
		return false;
	});

	$('.login-btn').click(function(){
			window.open('/accounts/login', "_self");
	});

	$('.signup-btn').click(function(){
			window.open('/accounts/signup', "_self");
	});

	$('.banner-signup-btn').click(function(){
			window.open('/accounts/signup', "_self");
	});



});
