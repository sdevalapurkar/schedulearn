$(document).ready(function() {
  // This script is used from this website and modified to suit our design needs:
  // https://www.jqueryscript.net/menu/Material-Design-Sliding-Tab-Menu-With-jQuery-CSS3.html

  $("#reviewTab").fadeOut(0);
  $("#historyTab").fadeOut(0);

  $("ul li").click(function(e) {

    // make sure we cannot click the slider
    if ($(this).hasClass('slider')) {
      return;
    }

    /* Add the slider movement */

    // what tab was pressed
    var clickedTab = $(this).index();

    // Work out how far the slider needs to go
    var sliderMovesBy = 120
    * clickedTab;

    $(".slider").css({
      left: sliderMovesBy + "px"
    });

    /* Add the ripple */

    // Remove olds ones
    $(".ripple").remove();

    // Setup
    var posX = $(this).offset().left,
    posY = $(this).offset().top,
    buttonWidth = $(this).width(),
    buttonHeight = $(this).height();

    // Add the element
    $(this).prepend("<span class='ripple'></span>");

    // Make it round!
    if (buttonWidth >= buttonHeight) {
      buttonHeight = buttonWidth;
    } else {
      buttonWidth = buttonHeight;
    }

    // Get the center of the element
    var x = e.pageX - posX - buttonWidth / 2;
    var y = e.pageY - posY - buttonHeight / 2;

    // Add the ripples CSS and start the animation
    $(".ripple").css({
      width: buttonWidth,
      height: buttonHeight,
      top: y + 'px',
      left: x + 'px'
    }).addClass("rippleEffect");
  });


  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-36251023-1']);
  _gaq.push(['_setDomainName', 'jqueryscript.net']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

  // This is my own jQuery code
  $("#avail").click(function(){
    $("#availabilityTable").delay(350).fadeIn(100);
    $("#reviewTab").fadeOut(300);
    $("#historyTab").fadeOut(300);
  });

  $("#revi").click(function(){
    $("#reviewTab").delay(350).fadeIn(100);
    $("#availabilityTable").fadeOut(300);
    $("#historyTab").fadeOut(300);
  });

  $("#hist").click(function(){
    $("#historyTab").delay(350).fadeIn(100);
    $("#availabilityTable").fadeOut(300);
    $("#reviewTab").fadeOut(300);
  });

  $('#notificationsDropdownLink').click(function() {
    var attr = $('#notificationIcon').attr('data-count');
    if (typeof attr !== typeof undefined && attr !== false) {
      $('#notificationIcon').removeAttr("data-count");
      $('#notificationIcon').removeClass("notification-badge");
    }
    $.ajax({
      url: '/dashboard/clear_notifications/',
      type: 'post',
      error: function(xhr, status) {
      },
      success: function(data) {
      }
    });
  });
});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});
