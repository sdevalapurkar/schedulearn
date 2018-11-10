$(document).ready(function() {
    $('#notifcationsDropdownLink').click(function() {
      var attr = $(this).attr('data-count');
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
