var img_url;

$(document).ready(function () {

  $('#logo').click(function() {
    window.open('/dashboard/', '_self');
  });

  $('#dashboard').click(function() {
    window.open('/dashboard/', '_self');
  });

  $('#scheduler').click(function() {
    window.open('/dashboard/scheduler', '_self');
  });

  $('#myProfile').click(function() {
    window.open('/dashboard/my_profile', '_self');
  });

  $('#copy').click(function() {
    var tutor_id = $("#ID");
    tutor_id.select();
    document.execCommand("copy");
  });

  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })

  var cropped = $("#crop_picture").croppie({
    viewport: {
        width: 200,
        height: 200,
        type: 'circle'
    }
  });

  $("#id_profile_pic").change(function () {
    $(".bd-crop-picture-modal-lg").modal();
    if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#crop_picture').attr('src', e.target.result);
            img_url = e.target.result;
        }
        reader.readAsDataURL(this.files[0]);
    }

  });

  $('.bd-crop-picture-modal-lg').on('shown.bs.modal', function (e) {
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
                    url: '/dashboard/my_profile/edit_profile_pic/',
                    data: {'profile_pic': resp},
                    success: function () {
                        location.reload();
                    }
                });

								$('.bd-crop-picture-modal-lg').modal('hide');
              })
  });

  $("#cancelCrop").on("click", function () {
    location.reload();
  });

  $(".text").on("click", function() {
    $("#id_profile_pic").click();
  });

  $('#edit_profile').click(function() {
    window.open('/dashboard/edit_profile', '_self');
  });


  $('#id_first_name').addClass("form-control");
  $('#id_last_name').addClass("form-control");
  $('#id_profile_pic').addClass("form-control-file");
  $('#id_profile_pic').attr('hidden', 'hidden');

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
