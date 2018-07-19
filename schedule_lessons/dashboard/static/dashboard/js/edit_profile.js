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
        type: 'circle'
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
                    url: '/dashboard/edit_profile/',
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
