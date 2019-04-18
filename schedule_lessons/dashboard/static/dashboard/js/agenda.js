$(document).ready(function () {
  $('[data-toggle="tooltip"]').tooltip();

  $(".acknowledge-btn").on('click', function(e) {
    var data;
    if (!$('#dontShowTutorialCheckbox').is(":checked")) {
      data = {
        'show_tutorial': 1, // true
      }
    } else {
      data = {
        'show_tutorial': 0, // false 
      };
    }
    $(".tutorial-wrapper").remove();
    $.ajax({
      url: '/dashboard/save_tutorial_preferences',
      type: 'post',
      data: data,
      error: function(xhr, status) {

      },
      success: function (data) {

      }

    });
  });

  $('#cancelLessonModal').on('show.bs.modal', function (e) {
    document.getElementById('cancelLessonConfirm').setAttribute("href", e.relatedTarget.href);
  });

  $('#options_btn').click(function(){
    $('.two-buttons').fadeToggle(300).toggleClass('addAnim');
    // $('#options_btn').toggleClass('addBtnAnim');
  });

  $('#declineLessonModal').on('show.bs.modal', function (e) {
    document.getElementById('declineLessonConfirm').setAttribute("href", e.relatedTarget.href);
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
