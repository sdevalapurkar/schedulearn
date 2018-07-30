$(document).ready(function() {

  $('#date').datetimepicker({
    format: 'L'
  });

  $('#startingTime').datetimepicker({
    format: 'LT'
  });

  $('#endingTime').datetimepicker({
    format: 'LT'
  });

  $("#addBtn").click(function() {
    $("#submit").click();
  });

});
