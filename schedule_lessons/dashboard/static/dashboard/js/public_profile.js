$(document).ready(function () {

  $('#copy').click(function() {
    var tutor_id = $("#ID");
    tutor_id.select();
    document.execCommand("copy");
  });

  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })

  $("#removeStudentBtn").on({
    mouseenter: function () {
      $("#removeStudentBtn").html("<i class='fas fa-user-minus extended-icon'></i>REMOVE STUDENT");
    },
    mouseleave: function () {
      $("#removeStudentBtn").html("<i class='fas fa-user-check extended-icon'></i>STUDENT ADDED");
    }
  });

  $("#removeTutorBtn").on({
    mouseenter: function () {
      $("#removeTutorBtn").html("<i class='fas fa-user-minus extended-icon'></i>REMOVE TUTOR");
    },
    mouseleave: function () {
      $("#removeTutorBtn").html("<i class='fas fa-user-check extended-icon'></i>TUTOR ADDED");
    }
  });

});
