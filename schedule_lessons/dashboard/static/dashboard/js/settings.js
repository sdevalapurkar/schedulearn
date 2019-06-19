$(document).ready(() => {
  $('#options_btn').click(() => {
    $('.two-buttons').fadeToggle(300).toggleClass('addAnim');
    $('#options_btn').toggleClass('addBtnAnim');
  });

  $('#secondNavBtn').click(() => {
    $('#navbarSupportedContent').slideToggle('fast');
  });

});