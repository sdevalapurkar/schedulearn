$(document).ready(function() {

  $('#startingTime').datetimepicker({
    format: 'LT'
  });

  $('#endingTime').datetimepicker({
    format: 'LT'
  });

  $("#addBtn").click(function() {
    $.ajax({
      url: '/dashboard/my_profile/edit_availability/',
      type: 'post',
      data: $('form#availabilityForm').serialize(),
      error: function(xhr, status) {
        $('.error-list').html('Something went wrong, please refresh and try again.');
      },
      success: function(data) {
        if (data['status'] == 200) {
          location.reload();
        } else {
          if (data['time_error']) {
            $('.error-list').html(data['time_error']);
            $('#startTimeLabel').addClass('label-error');
            $('#startTimeInput').addClass('input-error');
            $('#endTimeLabel').addClass('label-error');
            $('#endTimeInput').addClass('input-error');
          } else {
            if (data['starting_time_error']) {
              $('#startTimeLabel').addClass('label-error');
              $('#startTimeInput').addClass('input-error');
            }
            if (data['ending_time_error']) {
              $('#endTimeLabel').addClass('label-error');
              $('#endTimeInput').addClass('input-error');
            }
          }
        }
      },
    });
  });

  var offset = new Date().getTimezoneOffset();
  offset *= (-1)
  $('#timeZoneInput').attr('value', offset);

});
