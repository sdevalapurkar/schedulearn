$(document).ready(function () {
    $(function () {
        $('#startDatePicker').datetimepicker();
        $('#endDatePicker').datetimepicker();
    });

    $('#scheduleLessonModal').on('show.bs.modal', function (event) {
        let saveButton = $(this).find('#saveSchedule');
        saveButton.click(function () {
            let scheduleJSON = {};
            scheduleJSON.lessonName = $('#lessonName').val();
            scheduleJSON.lessonDescription = $('#lessonDescription').val();
            scheduleJSON.startDate = $('#startDatePicker').find('input').val();
            scheduleJSON.endDate = $('#endDatePicker').find('input').val();
        });
    });

    // $.get('home/get_tutors', function (data) {
    //     console.log('data', data);
    // });
});

function openMyProfile() {
    window.open('myProfile/my_profile.html');
}
