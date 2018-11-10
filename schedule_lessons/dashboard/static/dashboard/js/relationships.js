$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();

    $('#notifcationsDropdownLink').click(function() {
      var attr = $(this).attr('data-count');
      if (typeof attr !== typeof undefined && attr !== false) {
        $('#notificationIcon').removeAttr("data-count");
        $('#notificationIcon').removeClass("notification-badge");
      }
      $.ajax({
        url: '/dashboard/clear_notifications/',
        type: 'post',
        error: function(xhr, status) {
        },
        success: function(data) {
        }
      });
    });
});
