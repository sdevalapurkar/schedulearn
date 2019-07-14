$(document).ready(() => {
  $('#secondNavBtn').click(() => {
    $('#navbarSupportedContent').slideToggle('fast');
  });

  $('#deleteAccountConfirm').click(() => {
    $('#deleteAccountModal').modal('hide');
    $.ajax({
      type: 'DELETE',
      url: '/dashboard/my_profile/delete_account/',
      success: () => {
        document.location.href = "/";
      }
    });
  });

  $("#confirmChangePassword").click(() => {
    $.ajax({
      type: 'POST',
      url: '/dashboard/my_profile/change_password/',
      data: { 'old_password': $("#oldPasswordInput").val(), 'new_password1': $("#newPasswordInput1").val(), 'new_password2': $("#newPasswordInput2").val() },
      error: (xhr, status) => {
        $("#oldPasswordInput").html('');
        $("#newPasswordInput1").html('');
        $("#newPasswordInput2").html('');
        $('.error-list').html('Something went wrong, please try again');
      },
      success: (response) => {
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
    // The data-count attribute will only exist if there are unread notifications.
    if ($('#notificationIcon').attr('data-count')) {
      $('#notificationIcon').removeAttr("data-count");
      $('#notificationIcon').removeClass("notification-badge");
      $.ajax({
        url: '/dashboard/clear_notifications/',
        type: 'POST'
      });
    }
  });

  $(".preference").click((event) => {
    const preference_id = event.target.id;
    $.ajax({
      type: "POST",
      url: "/dashboard/modify_preference/" + preference_id + "/",
      data: { "active": event.target.checked }
    });
  });
});

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
  // Sanity check
  if (!document.cookie) {
    return null;
  }

  // Search through the cookies to find the desired cookie.
  let cookieValue = null;
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
  }
  return cookieValue;
}

$.ajaxSetup({
  beforeSend: (xhr, settings) => {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    }
  }
});
