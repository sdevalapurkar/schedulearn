from django.shortcuts import render, redirect
import json
import datetime
from django.http import HttpResponse
from .models import Relationship, Event
from accounts.models import Profile
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
import base64
from django.core.files.base import ContentFile
from schedule_lessons.local_settings import *

# # used to set an event for a student. Later implementation will require another
# # method like this for tutors to set events, or it can be done in this method
# # using if-else to check for user_type of requesting user.
# @login_required
# def set_event(request):
#     if request.method == 'POST':
#         data = request.POST
#         try:
#             name = data.get('lessonName')
#             start_time = datetime.datetime.strptime(data.get('startDate'), '%m/%d/%Y %I:%M %p')
#
#             end_time = datetime.datetime.strptime(data.get('endDate'), '%m/%d/%Y %I:%M %p')
#
#             description = data.get('lessonDescription')
#             location = data.get('lessonLocation')
#             tutor = User.objects.get(profile__id=data.get('tutorID'))
#
#             event = Event(name=name, tutor=tutor, start_time = start_time, end_time = end_time, description=description, location=location, student=request.user)
#             event.save()
#
#             with get_connection(
#                 host=EMAIL_HOST,
#                 port=EMAIL_PORT,
#                 username=SCHEDULER_NOTIFY_EMAIL,
#                 password=EMAIL_HOST_PASSWORD,
#                 use_tls=True,
#             ) as connection:
#                 EmailMessage('Schedulearn: Lesson scheduled by ' + request.user.first_name + ' ' + request.user.last_name,
#                              'A student of yours, ' + request.user.first_name + ' ' + request.user.last_name + ', has booked a lesson with you with the following details, please visit schedulearn.com/ to either accept or decline the lesson.\n\n' + 'Lesson Name: '  + str(name) + '\n\nLesson Description: ' + str(description) + '\n\nLesson Timings: ' + 'From ' + str(start_time) + ' to ' + str(end_time) + '\n\nLesson Location: ' + location,
#                              local_settings.SCHEDULER_NOTIFY_EMAIL,
#                              [tutor.email],
#                              connection=connection).send()
#
#             return HttpResponse(status=200)
#         except Exception as e:
#             return HttpResponse(status=404)
#     else:
#         return HttpResponse(status=404)

# # renders the availability page for a tutor. login_required decorator is not
# # used so public can see availability too.
# def get_availability(request, tutor_id):
#     if request.method == 'GET':
#         tutor = User.objects.get(profile__id=tutor_id)
#         availability = tutor.profile.availability
#         if tutor.profile.availability is not None:
#             availability = json.loads(tutor.profile.availability.replace("'", '"'))
#         if availability == {} or availability == '{}':
#             availability = None
#
#         return render(request, 'dashboard/availability.html', {'availability': availability, 'user_full_name': tutor.get_full_name()})
#     return HttpResponse(status=404)

# # I don't think this method is even being used? Further inspection necessary.
# def set_availability(request):
#     if request.method == 'POST':
#         data = request.body
#         try:
#             tutor = User.objects.get(profile__id=data.get('id'))
#             tutor.profile.availability = data.get('data')
#             tutor.save()
#             return HttpResponse(status=200)
#         except Exception as e:
#             pass
#
#     return HttpResponse(status=404)

# # allows to edit availability for tutor.
# @login_required
# def edit_availability(request):
#     if request.method == 'POST':
#         data = request.POST
#         try:
#             current_user = User.objects.get(id=request.user.id)
#             availability = request.user.profile.availability
#             if availability is not None:
#                 current = json.loads(availability.replace("'", '"'))
#             else:
#                 current = {}
#             current.update(data.dict())
#             current_user.profile.availability = current
#             current_user.save()
#             return HttpResponse(status=200)
#
#         except Exception as e:
#             pass
#
#     return HttpResponse(status=404)


# returns scheduler information for scheduler tab for the user.
@login_required
def agenda(request):
    if request.method == 'GET':
        user_type = request.user.profile.user_type

        pending_event_list = []
        scheduled_event_list = []
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
                    'start_shortdate': event.start_time.strftime('%B'),
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
                    scheduled_event_list.append(data)
            except Exception as e:
                pass
        return render(request, 'dashboard/agenda.html', {'scheduled_events': scheduled_event_list, 'pending_events': pending_event_list})

    return HttpResponse(status=404)

# will get executed when a student tries to go to the tutors page.
# method will return a list of tutors that the student has added.
@login_required
def tutors(request):
    tutors = []
    relationships = Relationship.objects.filter(student=request.user) # will return a list that is a list of tutors that the current student has added.
    for relationship in relationships:
        url = request.build_absolute_uri('/') + "dashboard/profile/" + str(relationship.tutor.profile.id)
        tutor_data = {
            'first_name': relationship.tutor.first_name,
            'last_name': relationship.tutor.last_name,
            'email': relationship.tutor.email,
            'profile_pic': relationship.tutor.profile.profile_pic,
            'public_profile_url': url,
        }
        tutors.append(tutor_data)
    no_results_found = request.GET.get('no_search_result')
    if no_results_found:
        return render(request, 'dashboard/tutors.html', {'tutors': tutors, 'no_results': 'No results were found'})
    return render(request, 'dashboard/tutors.html', {'tutors': tutors})

@login_required
def students(request):
    students = []
    relationships = Relationship.objects.filter(tutor=request.user) # will return a list that is a list of tutors that the current student has added.
    for relationship in relationships:
        url = request.build_absolute_uri('/') + "dashboard/profile/" + str(relationship.student.profile.id)
        student_data = {
            'first_name': relationship.student.first_name,
            'last_name': relationship.student.last_name,
            'email': relationship.student.email,
            'profile_pic': relationship.student.profile.profile_pic,
            'public_profile_url': url,
        }
        students.append(student_data)
    no_results_found = request.GET.get('no_search_result')
    if no_results_found:
        return render(request, 'dashboard/students.html', {'students': students, 'no_results': 'No results were found'})
    return render(request, 'dashboard/students.html', {'students': students})

@login_required
def search(request):
    email = request.GET['searchResult']
    try:
        user_result = User.objects.get(email__iexact=email)
        id = str(user_result.profile.id)
        url = request.build_absolute_uri('/') + "dashboard/profile/" + id
        return public_profile(request, id)
    except User.DoesNotExist as e:
        if request.user.profile.user_type == 'tutor':
            response = redirect('students')
            response['Location'] += '?no_search_result=False'
        else:
            response = redirect('tutors')
            response['Location'] += '?no_search_result=False'
        return response

def public_profile(request, id):
    try:
        profile_user = User.objects.get(profile__id=id) # get the user to which the profile belongs
        if not request.user.is_anonymous:
            if request.user.profile.user_type == 'tutor':
                if relationship_exists(profile_user, request.user):
                    remove_student_url = request.build_absolute_uri('/') + "dashboard/remove_student/" + str(id)
                    return render(request, 'dashboard/public_profile.html', {'profile_user': profile_user, 'rel_exists': True, 'remove_student_url':remove_student_url})
                else:
                    add_student_url = request.build_absolute_uri('/') + "dashboard/add_student/" + str(id)
                    return render(request, 'dashboard/public_profile.html', {'profile_user': profile_user, 'add_student_url': add_student_url})
            elif request.user.profile.user_type == 'student':
                if relationship_exists(request.user, profile_user):
                    remove_tutor_url = request.build_absolute_uri('/') + "dashboard/remove_tutor/" + str(id)
                    return render(request, 'dashboard/public_profile.html', {'profile_user': profile_user, 'rel_exists': True, 'remove_tutor_url':remove_tutor_url})
                else:
                    add_tutor_url = request.build_absolute_uri('/') + "dashboard/add_tutor/" + str(id)
                    return render(request, 'dashboard/public_profile.html', {'profile_user': profile_user, 'add_tutor_url': add_tutor_url})
        else:
            return render(request, 'dashboard/public_profile.html', {'profile_user': profile_user})


    except Exception as e:
        print(str(e))
        return HttpResponse(status=404) # replace with return of the error 404 page after it's made.

# viewing MY profile will be different than viewing somebody else's profile, hence
# a new view template and url will be set up for the feature of viewing someone else's profile.
@login_required
def my_profile(request):
    reset_email = request.GET.get('reset_email', False)
    if reset_email:
        return render(request, 'dashboard/my_profile.html', {'user': request.user, 'changed_email': True})
    else:
        return render(request, 'dashboard/my_profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        if 'profile_pic' in request.POST:
             cropped_img = request.POST['profile_pic']
             format, imgstr = cropped_img.split(';base64,')
             ext = format.split('/')[-1]
             cropped_img = ContentFile(base64.b64decode(imgstr), name='temp.' + ext) # You can save this as file instance.
             request.user.profile.profile_pic = cropped_img
             request.user.save()
             return HttpResponse(status=200)
        else:
            request.user.first_name = request.POST['firstName'] # save first name
            request.user.last_name = request.POST['lastName'] # save last name
            # then handle email
            email = request.POST['email']
            if not email == request.user.email: # if the emails are not same that means the user changed emails
                # send a mail
                request.user.email = email
                request.user.profile.email_verified = False
                id = request.user.profile.id
                url = request.build_absolute_uri('/') + "accounts/verify_email/" + str(id)
                with get_connection(
                    host=EMAIL_HOST,
                    port=EMAIL_PORT,
                    username=VERIFY_USER_EMAIL,
                    password=EMAIL_HOST_PASSWORD,
                    use_tls=True,
                ) as connection:
                    EmailMessage("Schedulearn - Verify Your Email Address",
                                 "Click on the following link to verify your email address\n\n" + url,
                                 VERIFY_USER_EMAIL,
                                 [email],
                                 connection=connection).send()
                request.user.save()
                response = redirect('my_profile')
                response['Location'] += '?reset_email=True'
                return response

            request.user.save()
            return redirect('my_profile')
    else:
        return render(request, 'dashboard/edit_profile.html', {'user': request.user})

@login_required
def add_student(request, id):
    student_profile = Profile.objects.get(id=id)
    new_rel = Relationship(student=student_profile.user, tutor=request.user)
    new_rel.save()
    return public_profile(request, id)

@login_required
def remove_student(request, id):
    student_profile = Profile.objects.get(id=id)
    old_rel = Relationship.objects.get(student=student_profile.user, tutor=request.user)
    old_rel.delete()
    return public_profile(request, id)

@login_required
def add_tutor(request, id):
    tutor_profile = Profile.objects.get(id=id)
    new_rel = Relationship(student=request.user, tutor=tutor_profile.user)
    new_rel.save()
    return public_profile(request, id)

@login_required
def remove_tutor(request, id):
    tutor_profile = Profile.objects.get(id=id)
    old_rel = Relationship.objects.get(student=request.user, tutor=tutor_profile.user)
    old_rel.delete()
    return public_profile(request, id)

def relationship_exists(student, tutor):
    try:
        Relationship.objects.get(student=student, tutor=tutor)
        return True
    except:
        return False
