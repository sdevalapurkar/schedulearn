from django.shortcuts import render, redirect
import json
import datetime
from django.http import HttpResponse
from .forms import ProfileForm, NameForm
from .models import Relationship, Event
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import base64
from django.core.files.base import ContentFile
from schedule_lessons import local_settings

# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'dashboard.html') # if they try to go to website.com/dashboard, they'll get dashboard.html

# Create a relationship between the student and a tutor
@login_required
def add_tutor(request):
    print("working")
    if request.method == 'POST':
        print("post")
        tutor_email = request.POST.get('tutor_email')
        print(tutor_email)
        try:
            try:
                # checks where there is already such an existing relationship.
                existing_rel = Relationship.objects.get(student=request.user, tutor=User.objects.get(email=tutor_email))
                return HttpResponse(status=200)

            except Exception as e:
                # if it doesn't a new one is created.
                new_rel = Relationship(student=request.user, tutor=User.objects.get(email=tutor_email))
                new_rel.save()
                return HttpResponse(status=200)
        # if the above code isn't successfully executed. An error 404 is sent back.
        except Exception as e:
            return HttpResponse(status=404)
    return HttpResponse(status=404)


# Return list of tutors that have Relationship with the student that is asking
# for the list of tutors.
@login_required
def get_tutors(request):
    if request.method == 'GET':
        response = []
        # below code will return a list of relationshion objects containing the
        # name of student and tutor
        students_tutors = Relationship.objects.filter(student=request.user)
        if request.user.profile.user_type == 'student':
            for tutor in students_tutors:
                response.append([tutor.tutor.first_name, tutor.tutor.last_name, tutor.tutor.profile.id, tutor.tutor.email])
        else:
            # this part of the code will never be executed right now because
            # a tutor is not able to look at his students, but because of future
            # implementation it is left in.
            for tutor in students_tutors:
                response.append([tutor.student.first_name, tutor.student.last_name, tutor.student.profile.id, tutor.tutor.email])

        return JsonResponse(response, safe=False)

# simply returns a Json object containing the list of events for the request user.
@login_required
def get_events(request):
    if request.method == 'GET':
        event_list = []

        events = Event.objects.filter(student=request.user)

        for event in events:
            event_list.append({
                'name': event.name,
                'tutor_name': event.tutor.get_full_name(),
                'tutor_id': event.tutor.profile.id,
                'tutor_username': event.tutor.username,
                'student_name': event.student.get_full_name(),
                'student_id': event.student.profile.id,
                'student_username': event.student.username,
                'start_time': event.start_time,
                'end_time': event.end_time,
                'description': event.description
            })
        return JsonResponse(event_list, safe=False)
    return HttpResponse(status=404)


# used to set an event for a student. Later implementation will require another
# method like this for tutors to set events, or it can be done in this method
# using if-else to check for user_type of requesting user.
@login_required
def set_event(request):
    if request.method == 'POST':
        data = request.POST
        try:
            name = data.get('lessonName')
            start_time = datetime.datetime.strptime(data.get('startDate'), '%m/%d/%Y %I:%M %p')

            end_time = datetime.datetime.strptime(data.get('endDate'), '%m/%d/%Y %I:%M %p')

            description = data.get('lessonDescription')
            location = data.get('lessonLocation')
            tutor = User.objects.get(profile__id=data.get('tutorID'))

            event = Event(name=name, tutor=tutor, start_time = start_time, end_time = end_time, description=description, location=location, student=request.user)
            event.save()

            with get_connection(
                host=EMAIL_HOST,
                port=EMAIL_PORT,
                username=SCHEDULER_NOTIFY_EMAIL,
                password=EMAIL_HOST_PASSWORD,
                use_tls=True,
            ) as connection:
                EmailMessage('Schedulearn: Lesson scheduled by ' + request.user.first_name + ' ' + request.user.last_name,
                             'A student of yours, ' + request.user.first_name + ' ' + request.user.last_name + ', has booked a lesson with you with the following details, please visit schedulearn.com/ to either accept or decline the lesson.\n\n' + 'Lesson Name: '  + str(name) + '\n\nLesson Description: ' + str(description) + '\n\nLesson Timings: ' + 'From ' + str(start_time) + ' to ' + str(end_time) + '\n\nLesson Location: ' + location,
                             local_settings.SCHEDULER_NOTIFY_EMAIL,
                             [tutor.email],
                             connection=connection).send()

            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=404)

# renders the availability page for a tutor. login_required decorator is not
# used so public can see availability too.
def get_availability(request, tutor_id):
    if request.method == 'GET':
        tutor = User.objects.get(profile__id=tutor_id)
        availability = tutor.profile.availability
        if tutor.profile.availability is not None:
            availability = json.loads(tutor.profile.availability.replace("'", '"'))
        if availability == {} or availability == '{}':
            availability = None

        return render(request, 'availability.html', {'availability': availability, 'user_full_name': tutor.get_full_name()})
    return HttpResponse(status=404)

# I don't think this method is even being used? Further inspection necessary.
def set_availability(request):
    if request.method == 'POST':
        data = request.body
        try:
            tutor = User.objects.get(profile__id=data.get('id'))
            tutor.profile.availability = data.get('data')
            tutor.save()
            return HttpResponse(status=200)
        except Exception as e:
            pass

    return HttpResponse(status=404)

# allows to edit availability for tutor.
@login_required
def edit_availability(request):
    if request.method == 'POST':
        data = request.POST
        try:
            current_user = User.objects.get(id=request.user.id)
            availability = request.user.profile.availability
            if availability is not None:
                current = json.loads(availability.replace("'", '"'))
            else:
                current = {}
            current.update(data.dict())
            current_user.profile.availability = current
            current_user.save()
            return HttpResponse(status=200)

        except Exception as e:
            pass

    return HttpResponse(status=404)


# returns scheduler information for scheduler tab for the user.
@login_required
def scheduler(request):
    if request.method == 'GET':
        user_type = request.user.profile.user_type

        pending_event_list = []
        event_list = []
        if user_type == 'student':
            events = Event.objects.filter(student=request.user)
        else:
            events = Event.objects.filter(tutor=request.user)
        for event in events:
            try:
                data = {
                    'id': event.id,
                    'name': event.name,
                    'location': event.location,
                    'tutor_name': event.tutor.get_full_name(),
                    'tutor_id': event.tutor.profile.id,
                    'tutor_username': event.tutor.username,
                    'student_name': event.student.get_full_name(),
                    'student_id': event.student.profile.id,
                    'student_username': event.student.username,
                    'start_date': event.start_time,
                    'end_date': event.end_time,
                    'start_shortdate': event.start_time.strftime('%B, %Y'),
                    'start_week_day': event.start_time.strftime('%A'),
                    'start_month_day': event.start_time.strftime('%d'),
                    'start_time': event.start_time.strftime('%I:%M %p'),
                    'end_shortdate': event.end_time.strftime('%B, %Y'),
                    'end_week_day': event.end_time.strftime('%A'),
                    'end_month_day': event.end_time.strftime('%d'),
                    'end_time': event.end_time.strftime('%I:%M %p'),
                    'description': event.description
                }
                if event.pending:
                    pending_event_list.append(data)
                else:
                    event_list.append(data)
            except Exception as e:
                pass
        return render(request, 'scheduler.html', {'user_type': user_type, 'events': event_list, 'pending_events': pending_event_list})

    return HttpResponse(status=404)

def public_profile(request, id):
    try:
        user = User.objects.get(profile__id=id) # get the user to which the profile belongs
        return render(request, 'public_profile.html', {'user': user, 'host': request.user})
    except:
        return HttpResponse(status=404) # replace with return of the error 404 page after it's made.

# viewing MY profile will be different than viewing somebody else's profile, hence
# a new view template and url will be set up for the feature of viewing someone else's profile.
@login_required
def my_profile(request):
    return render(request, 'my_profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        print("Got here")
        if 'profile_pic' in request.POST:
             cropped_img = request.POST['profile_pic']
             format, imgstr = cropped_img.split(';base64,')
             ext = format.split('/')[-1]
             cropped_img = ContentFile(base64.b64decode(imgstr), name='temp.' + ext) # You can save this as file instance.
             request.user.profile.profile_pic = cropped_img
             request.user.save()
             return HttpResponse(status=200)
        else:
            name_form = NameForm(request.POST, instance=request.user)
            if name_form.is_valid():
                request.user.first_name = name_form.cleaned_data['first_name']
                request.user.last_name = name_form.cleaned_data['last_name']
                request.user.save()
            return render(request, 'my_profile.html', {'user': request.user})
    else:
        profile_form = ProfileForm()
        name_form = NameForm()
        return render(request, 'edit_profile.html', {'user': request.user, 'profile_form': profile_form, 'name_form': name_form})


# will return the user_type for the current user.
@login_required
def user_type(request):
    if request.method == 'GET':
        return JsonResponse({'user_type': request.user.profile.user_type, 'id': request.user.profile.id})
    return HttpResponse(status=404)

@login_required
def confirm_lesson(request):
    if request.method == 'POST':
        event_id = request.POST.get('id')
        event = Event.objects.get(id=event_id)
        event.pending = False
        event.save()
        return HttpResponse(status=200)
    return HttpResponse(status=404)


@login_required
def decline_lesson(request):
    if request.method == 'POST':
        event_id = request.POST.get('id')
        Event.objects.get(id=event_id).delete()
        return HttpResponse(status=200)
    return HttpResponse(status=404)
