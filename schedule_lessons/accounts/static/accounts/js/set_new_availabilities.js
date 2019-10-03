$(document).ready(() => {
  $('#goToFindTutor').click(() => {
    $('#setAvailability')
      .delay(300)
      .fadeOut(0)
      .addClass('slide-away');
    $('#findTutor')
      .delay(350)
      .addClass('slide-in')
      .fadeIn(0);
    $('#goToFindTutor').fadeOut(350);
    $('#backToAgenda').html(
      '<i class="far fa-calendar extended-icon"></i>SCHEDULE A LESSON'
    );
  });
});
