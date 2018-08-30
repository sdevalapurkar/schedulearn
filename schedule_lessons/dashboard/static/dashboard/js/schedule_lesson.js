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
    let form_data = $('form#scheduleForm').serialize() + "&timezoneInfo=" + (new Date().getTimezoneOffset() * -1);
    $.ajax({
      url: window.location.href,
      type: 'post',
      data: form_data,
      error: function(xhr, status) {
        $('#scheduleVerification').html('');
        $('.error-list').html('Something went wrong, please make sure your information is correct and try again.');
        $('#titleLabel').addClass('label-error');
        $('#titleInput').addClass('input-error');
        $('#locationLabel').addClass('label-error');
        $('#locationInput').addClass('input-error');
        $('#dateLabel').addClass('label-error');
        $('#dateInput').addClass('input-error');
        $('#startTimeLabel').addClass('label-error');
        $('#startTimeInput').addClass('input-error');
        $('#endTimeLabel').addClass('label-error');
        $('#endTimeInput').addClass('input-error');
      },
      success: function(data) {
        console.log(data);
        if (data['status'] == 200) {
          $('#scheduleVerification').html(data['schedule_success']);
          $('#titleLabel').removeClass('label-error');
          $('#titleInput').removeClass('input-error');
          $('#locationLabel').removeClass('label-error');
          $('#locationInput').removeClass('input-error');
          $('#dateLabel').removeClass('label-error');
          $('#dateInput').removeClass('input-error');
          $('#startTimeLabel').removeClass('label-error');
          $('#startTimeInput').removeClass('input-error');
          $('#endTimeLabel').removeClass('label-error');
          $('#endTimeInput').removeClass('input-error');
          $('.error-list').html('');
        } else {
          if (data['name_error']) {
            $('#titleLabel').addClass('label-error');
            $('#titleInput').addClass('input-error');
          } else {
            $('#titleLabel').removeClass('label-error');
            $('#titleInput').removeClass('input-error');
          }
          if (data['location_error']) {
            $('#locationLabel').addClass('label-error');
            $('#locationInput').addClass('input-error');
          } else {
            $('#locationLabel').removeClass('label-error');
            $('#locationInput').removeClass('input-error');
          }
          if (data['date_error']) {
            $('#dateLabel').addClass('label-error');
            $('#dateInput').addClass('input-error');
          } else {
            $('#dateLabel').removeClass('label-error');
            $('#dateInput').removeClass('input-error');
          }
          if (data['starting_time_error']) {
            $('#startTimeLabel').addClass('label-error');
            $('#startTimeInput').addClass('input-error');
          } else {
            $('#startTimeLabel').removeClass('label-error');
            $('#startTimeInput').removeClass('input-error');
          }
          if (data['ending_time_error']) {
            $('#endTimeLabel').addClass('label-error');
            $('#endTimeInput').addClass('input-error');
          } else {
            $('#endTimeLabel').removeClass('label-error');
            $('#endTimeInput').removeClass('input-error');
          }
          $('.error-list').html(data['time_error']);
        }
      },
    });
  });

});
