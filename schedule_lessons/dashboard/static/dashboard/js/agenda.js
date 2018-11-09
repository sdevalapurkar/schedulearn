$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();

    $('#cancelLessonModal').on('show.bs.modal', function (e) {
      document.getElementById('cancelLessonConfirm').setAttribute("href", e.relatedTarget.href);
    });

    $('#declineLessonModal').on('show.bs.modal', function (e) {
      document.getElementById('declineLessonConfirm').setAttribute("href", e.relatedTarget.href);
    });
});
