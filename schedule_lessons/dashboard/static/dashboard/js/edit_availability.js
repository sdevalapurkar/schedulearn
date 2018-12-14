$(document).ready(function () {

  $('#startingTime').datetimepicker({
    format: 'LT'
  });

  $('#endingTime').datetimepicker({
    format: 'LT'
  });

  $("#addBtn").click(function () {
    let form_data = $('form#availabilityForm').serialize() + "&timezoneInfo=" + (new Date().getTimezoneOffset() * -1);
    $.ajax({
      url: '/dashboard/my_profile/edit_availability/',
      type: 'post',
      data: form_data,
      error: function (xhr, status) {
        $('.error-list').html('Something went wrong, please make sure your information is correct and try again.');
        $('#startTimeLabel').addClass('label-error');
        $('#startTimeInput').addClass('input-error');
        $('#endTimeLabel').addClass('label-error');
        $('#endTimeInput').addClass('input-error');
      },
      success: function (data) {
        if (data['status'] == 200) {
          location.reload();
        } else {
          if (data['time_error']) {
            $('.error-list').html(data['time_error']);
            $('#startTimeLabel').addClass('label-error');
            $('#startTimeInput').addClass('input-error');
            $('#endTimeLabel').addClass('label-error');
            $('#endTimeInput').addClass('input-error');
          } else {
            if (data['starting_time_error']) {
              $('#startTimeLabel').addClass('label-error');
              $('#startTimeInput').addClass('input-error');
            }
            if (data['ending_time_error']) {
              $('#endTimeLabel').addClass('label-error');
              $('#endTimeInput').addClass('input-error');
            }
          }
        }
      },
    });
  });

  $('#notificationsDropdownLink').click(function () {
    var attr = $('#notificationIcon').attr('data-count');
    if (typeof attr !== typeof undefined && attr !== false) {
      $('#notificationIcon').removeAttr("data-count");
      $('#notificationIcon').removeClass("notification-badge");
    }
    $.ajax({
      url: '/dashboard/clear_notifications/',
      type: 'post',
      error: function (xhr, status) {
      },
      success: function (data) {
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
  beforeSend: function (xhr, settings) {
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
      // Only send the token to relative URLs i.e. locally.
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
  }
});
