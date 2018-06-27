$(document).ready(function () {
  var img_url;
  var csrftoken = getCookie('csrftoken');

  $(".id_profile_pic").change(function () {
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

  var cropped = $("#crop_picture").croppie({
    viewport: {
        width: 200,
        height: 200,
        type: 'circle'
    }
  });

  $('.bd-crop-picture-modal-lg').on('shown.bs.modal', function (e) {
    cropped.croppie('bind', {
      url: img_url,
    });
  })

  $("#saveCrop").on("click", function(ev) {
    cropped.croppie('result', {
								type: 'base64',
								format: 'jpeg',
								size: {width: 200, height: 200}
							}).then(function (resp) {
                console.log(csrftoken)
                $.ajax({
                  type: 'POST',
                  url: '/accounts/personalize/',
                  data: {'profile_pic': resp},
                  beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                      xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                  }
                });

                var base64 = "url(" + resp + ")";
                $(".picture").css('background-image', base64);
                $(".id_profile_pic").val('');
								$('.bd-crop-picture-modal-lg').modal('hide');
              })
  });

  $("#cancelCrop").on("click", function () {
    $('.bd-crop-picture-modal-lg').modal('hide');
    $(".id_profile_pic").val('');
  });

  $(".camera-icon").on("click", function() {
    $(".id_profile_pic").click();
  });

  $(".continue-btn").on("click", function() {
    $(".submit").click();
  });


  // using jQuery
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


});
