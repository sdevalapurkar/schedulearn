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

  var timezoneInfo = new Date().toString().split(' ')[5].substring(3);
  $('#timeZoneInput').attr('value', timezoneInfo);

});
