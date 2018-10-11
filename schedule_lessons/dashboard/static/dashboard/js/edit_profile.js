var img_url;

$(document).ready(function () {

  $("#saveChanges").click(function() {
    $("#profileSave").click();
  });

  /* ALL CODE BELOW RELATED TO CROPPING PICTURE */

  var cropped = $("#cropPicture").croppie({
    viewport: {
        width: 200,
        height: 200,
        type: 'square'
    }
  });

  $("#inputPfp").change(function () {
    $("#cropPictureModal").modal();
    if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#cropPicture').attr('src', e.target.result);
            img_url = e.target.result;
        }
        reader.readAsDataURL(this.files[0]);
    }

  });

  $('#cropPictureModal').on('shown.bs.modal', function (e) {
    cropped.croppie('bind', {
      url: img_url,
      points: [77,469,280,739]
    });
  })

  $("#saveCrop").on("click", function(ev) {
    cropped.croppie('result', {
								type: 'base64',
								format: 'jpeg',
								size: {width: 200, height: 200}
							}).then(function (resp) {
                $.ajax({
                    type: 'POST',
                    url: '/dashboard/my_profile/edit_profile/',
                    data: {'profile_pic': resp},
                    success: function () {
                        location.reload();
                    }
                });

								$('#cropPictureModal').modal('hide');
              })
  });

  $(".text").on("click", function() {
    $("#inputPfp").click();
  });

  $("#confirmChangePassword").on("click", function() {
    $.ajax({
      type: 'POST',
      url: '/dashboard/my_profile/change_password/',
      data: {'old_password': $("#oldPasswordInput").val(), 'new_password1': $("#newPasswordInput1").val(), 'new_password2': $("#newPasswordInput2").val()},
      error: function(xhr, status) {
        $("#oldPasswordInput").html('');
        $("#newPasswordInput1").html('');
        $("#newPasswordInput2").html('');
        $('.error-list').html('Something went wrong, please try again');
      },
      success: function(response) {
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
