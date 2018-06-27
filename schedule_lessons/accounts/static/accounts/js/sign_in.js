$(document).ready(function() {
  $(".signup-btn").click(function() {
    window.open("/accounts/signup", "_self")
  });

  $(".continue-btn").on("click", function() {
    $(".submit").click();
  });


});
