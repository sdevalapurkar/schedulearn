$(document).ready(() => {
  $('[data-toggle="tooltip"]').tooltip();

  $('.acknowledge-btn').on('click', e => {
    let data = {
      show_tutorial: false
    };
    if (!$('#dontShowTutorialCheckbox').is(':checked')) {
      data.show_tutorial = true;
    }
    $('.tutorial-wrapper').remove();
    $.ajax({
      url: '/dashboard/save_tutorial_preferences/',
      type: 'post',
      data: data,
      error: (xhr, status) => {
        alert('Something went wrong, please try again.');
      }
    });
  });

  $('#cancelLessonModal').on('show.bs.modal', e => {
    document.getElementById('cancelLessonConfirm').setAttribute('href', e.relatedTarget.href);
  });

  $('#options_btn').click(() => {
    $('.two-buttons')
      .fadeToggle(300)
      .toggleClass('addAnim');
    $('#options_btn').toggleClass('addBtnAnim');
  });

  $('#secondNavBtn').click(() => {
    $('#navbarSupportedContent').slideToggle('fast');
  });

  $('#declineLessonModal').on('show.bs.modal', e => {
    document.getElementById('declineLessonConfirm').setAttribute('href', e.relatedTarget.href);
  });

  $('#notificationsDropdownLink').click(() => {
    const attr = $('#notificationIcon').attr('data-count');
    if (typeof attr !== typeof undefined && attr !== false) {
      $('#notificationIcon').removeAttr('data-count');
      $('#notificationIcon').removeClass('notification-badge');
    }
    $.ajax({
      url: '/dashboard/clear_notifications/',
      type: 'post',
      error: (xhr, status) => {},
      success: data => {}
    });
  });
});

const getCookie = name => {
  let cookieValue = null;
  if (document.cookie && document.cookie != '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

$.ajaxSetup({
  beforeSend: (xhr, settings) => {
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
      // Only send the token to relative URLs i.e. locally.
      xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    }
  }
});
