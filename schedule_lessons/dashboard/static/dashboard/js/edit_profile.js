var img_url;

$(document).ready(function () {
  $('#notificationsDropdownLink').click(function() {
    var attr = $('#notificationIcon').attr('data-count');
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

  $("#myTags").tagit({
    availableTags: ["Elementary Math", "Pre-Algebra", "Algebra I", "Algebra II",
                    "Geometry", "Trigonometry", "Pre-Calculus", "Calculus AB",
                    "Calculus BC", "Statistics", "Discrete Math", "Biology",
                    "Elementary Science", "Middle Grades Science", "Chemistry",
                    "Environmental Science", "Anatomy & Physiology", "Physics",
                    "Physics B", "Physics C: Electricity and Magnetism",
                    "Physics C: Mechanics", "Computer Science", "English Language",
                    "English as a Second Language", "English Literature",
                    "Reading Comprehension", "Critical Reading", "Writing",
                    "College Essay Writing", "French", "Italian", "Spanish",
                    "German", "Spanish Literature", "Japanese", "Latin",
                    "U.S. History", "Macroeconomics", "Microeconomics",
                    "World History", "European History", "Human Geography",
                    "Art History", "Psychology", "Elementary Social Studies",
                    "Music Theory", "Middle School Social Studies",
                    "Reading Comprehension", "Writing", "Reading Speed",
                    "College Essay Writing", "Critical Reading"],
  removeConfirmation: true,
  allowSpaces: true
  });


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
        url: '/dashboard/my_profile/edit_profile/',
        data: {'profile_pic': resp},
        success: function () {location.reload();}
      });
    
      $('#cropPictureModal').modal('hide');
    });
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
