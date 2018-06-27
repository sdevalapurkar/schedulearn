$(document).ready(function () {

  $('#dashboard').click(function() {
    window.open('/dashboard/', '_self');
  });

  $('#scheduler').click(function() {
    window.open('/dashboard/scheduler', '_self');
  });

  $('#copy').click(function() {
    var tutor_id = $("#ID");
    tutor_id.select();
    document.execCommand("copy");
  });

  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })

  $('#edit_profile').click(function() {
    window.open('/dashboard/edit_profile', '_self');
  });
});
