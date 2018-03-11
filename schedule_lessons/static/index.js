let tutorID = undefined;

$(document).ready(function () {
    let url = window.location.pathname;
    tutorID = url.replace('/home/availability/', '');

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
            scheduleJSON.tutorID = tutorID;

            console.log(scheduleJSON);

            $.ajax({
                type: 'POST',
                url: '/home/set_event',
                data: scheduleJSON
            });
        });
    });

    $.get('get_tutors', function (data) {
        if (data.length < 200) {
            console.log(data);
            var content = "<table>";
            content += '<th>' + 'First Name' + '</th>'+'<th>' + 'Last Name' + '</th>'+'<th>' + 'Check Availability' + '</th>';
            for (i = 0; i < data.length; i++) {
                // content += '<tr>'+'<td>' + data[i][0] + '</td>'+'<td>' + data[i][1] + '</td>'+'</tr>';
                content += '<tr>' +'<td>' + data[i][0] + '</td>'+'<td>' + data[i][1] + '</td>' +'<td>' + '<a href='+ '/home/availability/' + data[i][2] + '>' + '<p>' + 'Show Open Time Slots' + '</p>' + '</a>' + '</td>' + '</tr>';
            }
            content += "</table>";
            $('#tutors-table').append(content);
        }
    });
});

function openMyProfile() {
    window.open('myProfile/my_profile.html');
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?

            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});
