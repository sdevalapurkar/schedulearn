$(document).ready(function () {

  $('#copy').click(function() {
    var tutor_id = $("#ID");
    tutor_id.select();
    document.execCommand("copy");
  });

  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })

  $("#removeStudentBtn").mouseover(function() {
    $("#removeStudentBtn").html("<i class='fas fa-user-minus extended-icon'></i>REMOVE STUDENT");
  });

  $("#removeStudentBtn").mouseleave(function() {
    $("#removeStudentBtn").html("<i class='fas fa-user-check extended-icon'></i>STUDENT ADDED");
  });

  $("#removeTutorBtn").mouseover(function() {
    $("#removeTutorBtn").html("<i class='fas fa-user-minus extended-icon'></i>REMOVE TUTOR");
  });

  $("#removeTutorBtn").mouseleave(function() {
    $("#removeTutorBtn").html("<i class='fas fa-user-check extended-icon'></i>TUTOR ADDED");
  });

});
