$(document).ready(function() {
  $(".login-btn").click(function() {
    window.open("/accounts/login", "_self")
  });

  $(".continue-btn").click(function() {
    $(".submit").click();
  });
});
