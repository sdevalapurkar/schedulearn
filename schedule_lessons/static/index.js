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

    $.get('get_tutors', function (data) {
        console.log(data);
        var content = "<table>";
        content += '<th>' + 'First Name' + '</th>'+'<th>' + 'Last Name' + '</th>'+'<th>' + 'Check Availability' + '</th>';
        for (i = 0; i < 3; i++) {
            // content += '<tr>'+'<td>' + data[i][0] + '</td>'+'<td>' + data[i][1] + '</td>'+'</tr>';
            content += '<tr>' +'<td>' + 'thehhs' + '</td>'+'<td>' + 'sauce' + '</td>' +'<td>' + '<a href='+ '/home/availability/' + 'data[i][2]' + '>' + '<p>' + 'Show Open Time Slots' + '</p>' + '</a>' + '</td>' + '</tr>';
        }
        content += "</table>";
        $('#tutors-table').append(content);
    });
});

function openMyProfile() {
    window.open('myProfile/my_profile.html');
}
