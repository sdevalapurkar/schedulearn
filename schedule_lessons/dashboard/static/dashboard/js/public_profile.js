$(document).ready(function () {

  $('#copy').click(function() {
    var tutor_id = $("#ID");
    tutor_id.select();
    document.execCommand("copy");
  });

  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })

});
