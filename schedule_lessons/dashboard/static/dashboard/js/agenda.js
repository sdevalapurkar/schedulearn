$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();

    $('#cancelLessonModal').on('show.bs.modal', function (e) {
      document.getElementById('cancelLessonConfirm').setAttribute("href", e.relatedTarget.href);
    });

    $('#declineLessonModal').on('show.bs.modal', function (e) {
      document.getElementById('declineLessonConfirm').setAttribute("href", e.relatedTarget.href);
    });

    $('#notifcationsDropdownLink').click(function() {
      if (document.getElementById("notificationIcon").hasAttribute("data-count")) {
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
