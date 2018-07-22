$('document').ready(function() {
  
  $("#searchInput").on("click", function() {
    $(this).removeClass('error-list');
  });

  $.ajax({
    type: 'GET',
    url: '/dashboard/get_profile_pic/',
    success: function (data) {
      $("#myPic").css("background-image", "url('/media/" + data + "')");
    }
  });

});
