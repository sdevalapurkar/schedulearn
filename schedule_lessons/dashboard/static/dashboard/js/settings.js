$(document).ready(function () {
  $('#options_btn').click(function () {
    $('.two-buttons').fadeToggle(300).toggleClass('addAnim');
    $('#options_btn').toggleClass('addBtnAnim');
  });

  $('#secondNavBtn').click(function () {
    $('#navbarSupportedContent').slideToggle('fast');
  });

});