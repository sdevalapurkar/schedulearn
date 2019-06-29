$(document).ready(() => {

  $('#secondNavBtn').click(() => {
    $('#navbarSupportedContent').slideToggle('fast');
  });

  $('#deleteAccountConfirm').click(() => {
    $('#deleteAccountModal').modal('hide');
    $.ajax({
      type: 'DELETE',
      url: '/dashboard/my_profile/delete_account/',
      success: function () {
        document.location.href = "/";
      }
    });
  });

  $("#confirmChangePassword").click(() => {
    $.ajax({
      type: 'POST',
      url: '/dashboard/my_profile/change_password/',
      data: { 'old_password': $("#oldPasswordInput").val(), 'new_password1': $("#newPasswordInput1").val(), 'new_password2': $("#newPasswordInput2").val() },
      error: function (xhr, status) {
        $("#oldPasswordInput").html('');
        $("#newPasswordInput1").html('');
        $("#newPasswordInput2").html('');
        $('.error-list').html('Something went wrong, please try again');
      },
      success: function (response) {
        if (response.status_code == 200) {
          window.location.href = window.location.href + "?password_change=True";
        } else {
          $("#changePasswordModal").modal('show');
          if (response.social_error) {
            $('.error-list').html(response.social_error);
          } else if (response.missing_field) {
            $('.error-list').html(response.missing_field);
          } else if (response.inequal_password) {
            $('.error-list').html(response.inequal_password);
          } else if (response.invalid_old_password) {
            $('.error-list').html(response.invalid_old_password);
          }
        }
      },
    })
  }); // click handler END for #confirmChangePassword

  $('#notificationsDropdownLink').click(() => {
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
