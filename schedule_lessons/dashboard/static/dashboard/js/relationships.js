$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();

    $('#notifcationsDropdownLink').click(function() {
      if (document.getElementById("notificationIcon").hasAttribute("data-count")) {
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
