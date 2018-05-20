var tutor = undefined;

$(document).ready(function () {

  $('#logo').click(function() {
    window.open('/dashboard/', '_self');
  });

  $('#dashboard').click(function() {
    window.open('/dashboard/', '_self');
  });

  $('#copy').click(function() {
    var tutor_id = $("#ID");
    tutor_id.select();
    document.execCommand("copy");
  });

  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })


  $('#id_first_name').addClass("form-control");
  $('#id_last_name').addClass("form-control");
  $('#id_profile_pic').addClass("form-control-file");

  $.get('/dashboard/user_type', function (data) {
      let userType = data.user_type;
      tutor = data.id;
      if (userType === 'client') {
          if (document.getElementById("editAvailability")) {
              document.getElementById("editAvailability").style.display = "none";
          }
          if (document.getElementById('editAvailabilityButton')) {
              document.getElementById('editAvailabilityButton').style.display = "none";
          }
          if (document.getElementById("addTutor")) {
              document.getElementById("addTutor").style.display = "block";
          }
      } else {
          if (document.getElementById("myTutors")) {
              document.getElementById("myTutors").style.display = 'none';
          }
          if (document.getElementById("editAvailability")) {
              document.getElementById("editAvailability").style.display = "block";
          }
          if (document.getElementById('editAvailabilityButton')) {
              document.getElementById('editAvailabilityButton').style.display = 'block';
          }
          if (document.getElementById('scheduleLesson')) {
              document.getElementById('scheduleLesson').style.display = 'none';
          }
      }
  });

  $('#editAvailabilityButton').click(function(){
      window.open('/dashboard/availability/' + tutor, "_self");
  });

});
