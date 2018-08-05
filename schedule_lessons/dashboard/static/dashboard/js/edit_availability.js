$(document).ready(function() {

  $('#startingTime').datetimepicker({
    format: 'LT'
  });

  $('#endingTime').datetimepicker({
    format: 'LT'
  });

  $("#addBtn").click(function() {
    $("#submit").click();
  });

  var offset = new Date().getTimezoneOffset();
  offset *= (-1)
  $('#timeZoneInput').attr('value', offset);

});
