let tutorID = undefined;
let testUrl = undefined;
let tutor = undefined;

$(document).ready(function () {
    $('.sauce-confirm').click(function (event) {
        $.ajax({
            type: 'POST',
            url: '/home/confirm_lesson',
            data: {'id': event.currentTarget.id},
            success: function () {
                location.reload();
            }
        });
    });

    $('.sauce-decline').click(function (event) {
        $.ajax({
            type: 'POST',
            url: '/home/decline_lesson',
            data: {'id': event.currentTarget.id},
            success: function () {
                location.reload();
            }
        });
    });

    $('#myTutors').click(function (event) {
        $.get('get_tutors', function (data) {
            if (data.length < 200) {
                $('#tutors-table').empty();
                var content = "<table>";
                content += '<th>' + 'First Name' + '</th>'+'<th>' + 'Last Name' + '</th>'+'<th>' + 'Check Availability' + '</th>';
                for (i = 0; i < data.length; i++) {
                    content += '<tr>' +'<td>' + data[i][0] + '</td>'+'<td>' + data[i][1] + '</td>' +'<td>' + '<a href='+ '/home/availability/' + data[i][2] + '>' + '<p>' + 'Show Open Time Slots' + '</p>' + '</a>' + '</td>' + '</tr>';
                }
                content += "</table>";
                $('#tutors-table').append(content);
            }
        });
    });

    let url = window.location.pathname;
    testUrl = url.replace('/home/', '');
    tutorID = url.replace('/home/availability/', '');

    $.get('/home/user_type', function (data) {
        let userType = data.user_type;
        tutor = data.id;
        if (userType === 'client') {
            if (document.getElementById("editAvailability")) {
                document.getElementById("editAvailability").style.display = "none";
            }
            if (document.getElementById('editAvailabilityButton')) {
                document.getElementById('editAvailabilityButton').style.display = "none";
            }
            if (document.getElementById("addTutor")) {
                document.getElementById("addTutor").style.display = "block";
            }
        } else {
            if (document.getElementById("myTutors")) {
                document.getElementById("myTutors").style.display = 'none';
            }
            if (document.getElementById("editAvailability")) {
                document.getElementById("editAvailability").style.display = "block";
            }
            if (document.getElementById('editAvailabilityButton')) {
                document.getElementById('editAvailabilityButton').style.display = 'block';
            }
            if (document.getElementById('scheduleLesson')) {
                document.getElementById('scheduleLesson').style.display = 'none';
            }
        }
    });

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

            $('#scheduleLessonModal').modal('toggle');

            $.ajax({
                type: 'POST',
                url: '/home/set_event',
                data: scheduleJSON,
                success: function () {
                    window.open('/home', "_self");
                }
            });
        });
    });

    $('#addTutorModal').on('show.bs.modal', function (event) {
        let saveButton = $(this).find('#addTutorButton');
        saveButton.unbind().click(function () {
            let addedTutor = {};
            addedTutor.tutor_id = $('#tutorID').val();
            
            $('#addTutorModal').modal('toggle');

            $.ajax({
                type: 'POST',
                url: '/home/add_tutor',
                data: addedTutor
            });
        });
    });

    $('#editAvailabilityModal').on('show.bs.modal', function (event) {
        let saveButton = $(this).find('#saveAvailability');
        saveButton.unbind().click(function () {
            let availabilityJSON = {};
            let key = $('#day').val();
            let day = '' + $('#day').val() + '';
            let times = '' + $('#availableTimes').val() + '';
            availabilityJSON[key] = $('#availableTimes').val();
            
            var content = $('#availabilityTable');
            for (var i = 0; i < 1; i++) {
                content += '<tr>' +'<td>' + (day) + '</td>'+'<td>' + (times) + '</td>' + '</tr>';
                content += $('#availabilityTable');
            }
            $('#availabilityTable').append(content);

            $('#day').val('');
            $('#availableTimes').val('');
            $('#editAvailabilityModal').modal('toggle');
            sortTable($('#availabilityTable'),'asc');

            console.log(availabilityJSON);

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
    window.open('/home/my_profile', "_self");
}

function openAvailability() {
    window.open('/home/availability/' + tutor, "_self");
}

function renderHomepage() {
    window.open('/home', "_self");
}

function previewFile(){
    var preview = document.querySelector('img'); //selects the query named img
    var file    = document.querySelector('input[type=file]').files[0]; //sames as here
    var reader  = new FileReader();

    reader.onloadend = function () {
        preview.src = reader.result;
    }

    if (file) {
        reader.readAsDataURL(file); //reads the data as a URL
    } else {
        preview.src = "";
    }
}

previewFile();  //calls the function named previewFile()

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
