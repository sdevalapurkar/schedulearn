let tutorID = undefined;
let testUrl = undefined;

$(document).ready(function () {
    let url = window.location.pathname;
    testUrl = url.replace('/home/', '');
    tutorID = url.replace('/home/availability/', '');

    $(function () {
        $('#startDatePicker').datetimepicker();
        $('#endDatePicker').datetimepicker();
    });

    $('#scheduleLessonModal').on('show.bs.modal', function (event) {
        let saveButton = $(this).find('#saveSchedule');
        saveButton.unbind().click(function () {
            let scheduleJSON = {};
            scheduleJSON.lessonName = $('#lessonName').val();
            scheduleJSON.lessonDescription = $('#lessonDescription').val();
            scheduleJSON.startDate = $('#startDatePicker').find('input').val();
            scheduleJSON.endDate = $('#endDatePicker').find('input').val();
            scheduleJSON.tutorID = tutorID;

            $.ajax({
                type: 'POST',
                url: '/home/set_event',
                data: scheduleJSON
            });
        });
    });

    $('#editAvailabilityModal').on('show.bs.modal', function (event) {
        let saveButton = $(this).find('#saveAvailability');
        saveButton.unbind().click(function () {
            let availabilityJSON = {};
            availabilityJSON.day = $('#day').val();
            availabilityJSON.times = $('#availableTimes').val();
            
            var content = $('#availabilityTable');
            for (var i = 0; i < 1; i++) {
                content += '<tr>' +'<td>' + (availabilityJSON.day).toUpperCase() + '</td>'+'<td>' + (availabilityJSON.times).toUpperCase() + '</td>' + '</tr>';
                content += $('#availabilityTable');
            }
            $('#availabilityTable').append(content);

            availabilityJSON = {};
            $('#day').val('');
            $('#availableTimes').val('');
            $('#editAvailabilityModal').modal('toggle');
            sortTable($('#availabilityTable'),'asc');

            $.ajax({
                type: 'POST',
                url: '/home/edit_availability',
                data: availabilityJSON
            });
        });
    });

    if (testUrl === '') {
        $.get('get_tutors', function (data) {
            if (data.length < 200) {
                var content = "<table>";
                content += '<th>' + 'First Name' + '</th>'+'<th>' + 'Last Name' + '</th>'+'<th>' + 'Check Availability' + '</th>';
                for (i = 0; i < data.length; i++) {
                    content += '<tr>' +'<td>' + data[i][0] + '</td>'+'<td>' + data[i][1] + '</td>' +'<td>' + '<a href='+ '/home/availability/' + data[i][2] + '>' + '<p>' + 'Show Open Time Slots' + '</p>' + '</a>' + '</td>' + '</tr>';
                }
                content += "</table>";
                $('#tutors-table').append(content);
            }
        });
    }
});

function openMyProfile() {
    window.open('home/my_profile');
}

function sortTable(table, order) {
    console.log(table, order);
    var asc = order === 'asc',
        tbody = table.find('tbody');

    tbody.find('tr').sort(function(a, b) {
        if (asc) {
            return $('td:first', a).text().localeCompare($('td:first', b).text());
        } else {
            return $('td:first', b).text().localeCompare($('td:first', a).text());
        }
    }).appendTo(tbody);
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
