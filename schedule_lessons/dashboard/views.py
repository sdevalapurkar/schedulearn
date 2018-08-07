from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from accounts.models import Availability, return_availabilities
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import get_connection
from django.core.mail.message import EmailMessage
import base64
from django.core.files.base import ContentFile
from schedule_lessons.local_settings import *
from social_django.utils import load_strategy
import requests
from django.contrib.auth import login

# Global Variables

DAYS_OF_THE_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
UTC_ZONE = datetime.timezone(datetime.timedelta(0)) # A timezone object used to convert local times into UTC times.

# returns scheduler information for scheduler tab for the user.
@login_required
def agenda(request):
    if request.method == 'GET':
        # This if block makes sure that if the user has a google account, then create a calendar called My Lessons (Schedulearn) in their google calender
        if request.user.social_auth.filter(provider='google-oauth2'):
            headers = {
                "Authorization": "Bearer " + request.user.social_auth.get(provider='google-oauth2').get_access_token(load_strategy()),
            }
            insert_calendar_url = "https://www.googleapis.com/calendar/v3/calendars"
            list_calendar_url = "https://www.googleapis.com/calendar/v3/users/me/calendarList"
            user_calendars = requests.get(list_calendar_url, headers=headers).json()['items']
            schedulearn_calendar_exists = False

            for calendar in user_calendars:
                if calendar['summary'] == 'My Lessons (Schedulearn)':
                    schedulearn_calendar_exists = True
            if not schedulearn_calendar_exists:
                requests.post(insert_calendar_url, headers=headers, json={'summary': 'My Lessons (Schedulearn)', 'timeZone': 'Europe/London'})
        pending_lesson_list = []
        scheduled_lesson_list = []
        if request.user.profile.user_type == 'student':
            lessons = Lesson.objects.filter(student=request.user)
        else:
            lessons = Lesson.objects.filter(tutor=request.user)
        for lesson in lessons:
            try:
                data = {
                    'id': lesson.id,
                    'name': lesson.name,
                    'location': lesson.location,
                    'tutor_name': lesson.tutor.get_full_name(),
                    'tutor_id': lesson.tutor.profile.id,
                    'student_name': lesson.student.get_full_name(),
                    'student_id': lesson.student.profile.id,
                    'start_time': lesson.start_time,
                    'end_time': lesson.end_time,
                    'display_options': lesson.created_by != request.user,
                }
                if lesson.pending:
                    pending_lesson_list.append(data)
                else:
                    scheduled_lesson_list.append(data)
            except Exception as e:
                pass
        no_results_found = request.GET.get('no_search_result')
        if no_results_found:
            return render(request, 'dashboard/agenda.html', {'scheduled_lessons': scheduled_lesson_list, 'pending_lessons': pending_lesson_list, 'no_results': 'No results were found'})
        return render(request, 'dashboard/agenda.html', {'scheduled_lessons': scheduled_lesson_list, 'pending_lessons': pending_lesson_list})

    return HttpResponse(status=404)

@login_required
def relationships(request):
    if request.user.profile.user_type == 'tutor':
        students = []
        relationships = Relationship.objects.filter(tutor=request.user) # will return a list that is a list of tutors that the current student has added.
        for relationship in relationships:
            students.append(relationship.student)
        no_results_found = request.GET.get('no_search_result')
        if no_results_found:
            return render(request, 'dashboard/relationships.html', {'students': students, 'no_results': 'No results were found'})
        return render(request, 'dashboard/relationships.html', {'students': students})
    else:
        tutors = []
        relationships = Relationship.objects.filter(student=request.user) # will return a list that is a list of tutors that the current student has added.
        for relationship in relationships:
            tutors.append(relationship.tutor)
        no_results_found = request.GET.get('no_search_result')
        if no_results_found:
            return render(request, 'dashboard/relationships.html', {'tutors': tutors, 'no_results': 'No results were found'})
        return render(request, 'dashboard/relationships.html', {'tutors': tutors})

@login_required
def search(request):
    email = request.GET.get('searchResult')
    if not email:
        response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        response['Location'] += '?no_search_result=True'
        return response
    try:
        user_result = User.objects.get(email__iexact=email)
        id = str(user_result.profile.id)
        url = request.build_absolute_uri('/') + 'dashboard/profile/' + id
        return public_profile(request, id)
    except User.DoesNotExist as e:
        response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        response['Location'] += '?no_search_result=True'
        return response

def public_profile(request, user_id):
    try:
        context = {
            'profile_user': User.objects.get(profile__id=user_id), # get the user to which the profile belongs
            'availabilities': return_availabilities(user_id),
            'days_of_the_week': DAYS_OF_THE_WEEK
        }

        if not request.user.is_anonymous:
            # Returns a boolean value depending on whether a relationship
            # exists between Person A and Person B
            context['rel_exists'] = relationship_exists(context['profile_user'], request.user)
            if context['rel_exists']:
                if request.user.profile.user_type == 'tutor':
                    context['remove_student_url'] = request.build_absolute_uri('/') + 'dashboard/remove_student/' + str(user_id)
                else:
                    context['remove_tutor_url'] = request.build_absolute_uri('/') + 'dashboard/remove_tutor/' + str(user_id)
            else:
                if request.user.profile.user_type == 'tutor':
                    context['add_student_url'] = request.build_absolute_uri('/') + 'dashboard/add_student/' + str(user_id)
                else:
                    context['add_tutor_url'] = request.build_absolute_uri('/') + 'dashboard/add_tutor/' + str(user_id)

            return render(request, 'dashboard/public_profile.html', context)

    except Exception as e:
        return HttpResponse(status=404) # replace with return of the error 404 page after it's made.

@login_required
def add_student(request, student_id):
    student_profile = User.objects.get(profile__id=student_id)
    new_rel = Relationship(student=student_profile, tutor=request.user)
    new_rel.save()
    return redirect('public_profile', student_id)

@login_required
def remove_student(request, student_id):
    student_profile = User.objects.get(profile__id=student_id)
    old_rel = Relationship.objects.get(student=student_profile, tutor=request.user)
    old_rel.delete()
    return redirect('public_profile', student_id)

@login_required
def add_tutor(request, tutor_id):
    tutor_profile = User.objects.get(profile__id=tutor_id)
    new_rel = Relationship(student=request.user, tutor=tutor_profile)
    new_rel.save()
    return redirect('public_profile', tutor_id)

@login_required
def remove_tutor(request, tutor_id):
    tutor_profile = User.objects.get(profile__id=tutor_id)
    old_rel = Relationship.objects.get(student=request.user, tutor=tutor_profile)
    old_rel.delete()
    return redirect('public_profile', tutor_id)

@login_required
def choose_person(request):
        if request.user.profile.user_type == 'tutor':
            students = []
            relationships = Relationship.objects.filter(tutor=request.user) # will return a list that is a list of tutors that the current student has added.
            for relationship in relationships:
                url = request.build_absolute_uri('/') + 'dashboard/profile/' + str(relationship.student.profile.id)
                student_data = {
                    'first_name': relationship.student.first_name,
                    'last_name': relationship.student.last_name,
                    'email': relationship.student.email,
                    'profile_pic': relationship.student.profile.profile_pic,
                    'id': relationship.student.profile.id,
                }
                students.append(student_data)
            no_results_found = request.GET.get('no_search_result')
            if no_results_found:
                return render(request, 'dashboard/choose_person.html', {'students': students, 'no_results': 'No results were found'})
            return render(request, 'dashboard/choose_person.html', {'students': students})
        else:
            tutors = []
            relationships = Relationship.objects.filter(student=request.user) # will return a list that is a list of tutors that the current student has added.
            for relationship in relationships:
                url = request.build_absolute_uri('/') + 'dashboard/profile/' + str(relationship.tutor.profile.id)
                tutor_data = {
                    'first_name': relationship.tutor.first_name,
                    'last_name': relationship.tutor.last_name,
                    'email': relationship.tutor.email,
                    'profile_pic': relationship.tutor.profile.profile_pic,
                    'id': relationship.tutor.profile.id,
                }
                tutors.append(tutor_data)
            no_results_found = request.GET.get('no_search_result')
            if no_results_found:
                return render(request, 'dashboard/choose_person.html', {'tutors': tutors, 'no_results': 'No results were found'})
            return render(request, 'dashboard/choose_person.html', {'tutors': tutors})

@login_required
def schedule_lesson(request, user_id):
    context = {
        'user_id': user_id,
        'days_of_the_week': DAYS_OF_THE_WEEK,
        'status': 500
    }
    if request.method == 'POST':
        new_lesson = Lesson()
        context = error_check_and_save_lesson(request, new_lesson, context)
        return JsonResponse(context)
    else:
        context['person_to_schedule_with'] = User.objects.get(profile__id=context['user_id'])
        context['availabilities'] = return_availabilities(user_id)
        return render(request, 'dashboard/schedule_lesson.html', context)

@login_required
def confirm_lesson(request, lesson_id):
    try:
        lesson_to_confirm = Lesson.objects.get(id=lesson_id)
        if lesson_to_confirm and (lesson_to_confirm.tutor == request.user or lesson_to_confirm.student == request.user) and request.user != lesson_to_confirm.created_by:
            lesson_to_confirm.pending = False
            lesson_to_confirm.save()
        return redirect('agenda')
    except Exception:
        return redirect('agenda')

@login_required
def decline_lesson(request, lesson_id):
    try:
        lesson_to_delete = Lesson.objects.get(id=lesson_id)
        if lesson_to_delete and (lesson_to_delete.tutor == request.user or lesson_to_delete.student == request.user):
            lesson_to_delete.delete()
        return redirect('agenda')
    except Exception:
        return redirect('agenda')

@login_required
def reschedule_lesson(request, lesson_id):
    try:
        lesson_to_reschedule = Lesson.objects.get(id=lesson_id)
    except Exception:
        return HttpResponse(status=404)
    context = {
        'user_id': lesson_to_reschedule.student.profile.id if request.user.profile.user_type == 'tutor' else lesson_to_reschedule.tutor.profile.id,
        'days_of_the_week': DAYS_OF_THE_WEEK,
        'status': 500
    }
    if request.method == 'POST':
        context = error_check_and_save_lesson(request, lesson_to_reschedule, context)
        return JsonResponse(context)
    else:
        context['person_to_schedule_with'] = User.objects.get(profile__id=context['user_id'])
        if lesson_to_reschedule and (lesson_to_reschedule.tutor == request.user or lesson_to_reschedule.student == request.user):
            context['availabilities'] = return_availabilities(context['person_to_schedule_with'].profile.id)
            context['lesson_to_reschedule'] = {
                'name': lesson_to_reschedule.name,
                'location': lesson_to_reschedule.location,
                'start_time': lesson_to_reschedule.start_time,
                'end_time': lesson_to_reschedule.end_time,
            }
            return render(request, 'dashboard/schedule_lesson.html', context)
        else:
            return HttpResponse(status=404)

# viewing MY profile will be different than viewing somebody else's profile, hence
# a new view template and url will be set up for the feature of viewing someone else's profile.
@login_required
def my_profile(request):
    context = {
        'user': request.user,
        'availabilities': return_availabilities(request.user.profile.id),
        'reset_email': request.GET.get('reset_email', False),
        'days_of_the_week': DAYS_OF_THE_WEEK
    }
    if context['reset_email']:
        return render(request, 'dashboard/my_profile.html', context)
    else:
        return render(request, 'dashboard/my_profile.html', context)

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
            if not request.POST['lastName']:
                request.user.last_name = ' '
            else:
                request.user.last_name = request.POST['lastName'] # save last name
            request.user.profile.bio = request.POST['bio']
            # then handle email
            email = request.POST['email']
            if not email == request.user.email: # if the emails are not same that means the user changed emails
                # send a mail
                request.user.email = email
                request.user.profile.email_verified = False
                id = request.user.profile.id
                url = request.build_absolute_uri('/') + 'accounts/verify_email/' + str(id)
                with get_connection(
                    host=EMAIL_HOST,
                    port=EMAIL_PORT,
                    username=VERIFY_USER_EMAIL,
                    password=EMAIL_HOST_PASSWORD,
                    use_tls=True,
                ) as connection:
                    EmailMessage('Schedulearn - Verify Your Email Address',
                                 'Click on the following link to verify your email address\n\n' + url,
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
def edit_availability(request):
    context = {'days_of_the_week': DAYS_OF_THE_WEEK,
               'day': request.POST.get('day', ''),
               'start_time': request.POST.get('startingTime', ''),
               'end_time': request.POST.get('endingTime', ''),
               'status': 500}
    if request.method == 'POST':
        date = getDateFromDay(context['day']).date() # a date object with static date with the sole purpose of representing a day of the week.
        time_difference = datetime.timezone(datetime.timedelta(minutes=int(request.POST.get('timezoneInfo',''))))
        context['starting_time_error'] = False if context['start_time'] else True
        context['ending_time_error'] = False if context['end_time'] else True
        if context.get('ending_time_error') or context.get('starting_time_error'):
            return JsonResponse(context)
        else:
            start_time_naive = datetime.datetime.strptime(request.POST['startingTime'], '%I:%M %p').time() # time objects
            end_time_naive = datetime.datetime.strptime(request.POST['endingTime'], '%I:%M %p').time() # time objects
            start_time = datetime.datetime.combine(date, start_time_naive, time_difference) # datetime objects
            end_time = datetime.datetime.combine(date, end_time_naive, time_difference) # datetime objects
            if start_time > end_time:
                context['time_error'] = 'The starting time provided is greater than the end time. Please fix this.'
                return JsonResponse(context)
            # First check if provided availability overlaps with other availabilities
            existing_availabilities = Availability.objects.filter(profile__id=request.user.profile.id, day=context['day'])
            for availability in existing_availabilities:
                existing_start_time = availability.start_time
                existing_end_time = availability.end_time
                if (existing_start_time < end_time) and (existing_end_time > start_time):
                    context['time_error'] = 'The timings you provided overlap with other timings that you have set'
                    return JsonResponse(context)
            # If timings aren't overlapping, add availability to database.
            new_availability = Availability()
            new_availability.profile = request.user.profile
            new_availability.start_time = start_time.astimezone(UTC_ZONE)
            new_availability.end_time = end_time.astimezone(UTC_ZONE)
            new_availability.day = context['day']
            new_availability.save()
            context['status'] = 200
            return JsonResponse(context)
    else:
        context['availabilities'] = return_availabilities(request.user.profile.id)
        return render(request, 'dashboard/edit_availability.html', context)

@login_required
def delete_availability(request, availability_id):
    try:
        delete_day = Availability.objects.get(profile__id=request.user.profile.id, id=availability_id)
        delete_day.delete()
        return redirect('edit_availability')
    except:
        return HttpResponse(status=404)

# Error Checking Functions

def error_check_and_save_lesson(request, lesson, context):
    person_to_schedule_with = User.objects.get(profile__id=context['user_id'])
    # Get lesson timezone when (re)scheduling lessons
    time_difference = datetime.timezone(datetime.timedelta(minutes=int(request.POST.get('timezoneInfo',''))))
    # Get lesson name when (re)scheduling lessons
    if not request.POST['name']:
        context['name_error'] = True
    else:
        lesson.name = request.POST['name']
    # Get lesson location when (re)scheduling lessons
    if not request.POST['location']:
        context['location_error'] = True
    else:
        lesson.location = request.POST['location']
    # Get lesson date when (re)scheduling lessons
    if not request.POST['date']:
        context['date_error'] = True
    else:
        date = datetime.datetime.strptime(request.POST['date'], '%m/%d/%Y').date() # a date object.
    # Get lesson starting time when (re)scheduling lessons
    if not request.POST['startingTime']:
        context['starting_time_error'] = True
    else:
        start_time = datetime.datetime.strptime(request.POST['startingTime'], '%I:%M %p').time() # a time object
    # Get lesson ending time when (re)scheduling lessons
    if not request.POST['endingTime']:
        context['ending_time_error'] = True
    else:
        end_time = datetime.datetime.strptime(request.POST['endingTime'], '%I:%M %p').time()
    if start_time > end_time:
        context['time_error'] = 'The starting time provided is greater than the end time. Please fix this.'

    lesson.tutor = request.user if request.user.profile.user_type == 'tutor' else person_to_schedule_with
    lesson.student = request.user if request.user.profile.user_type == 'student' else person_to_schedule_with

    if not context.get('name_error') and not context.get('location_error') and not context.get('date_error') and not context.get('starting_time_error') and not context.get('ending_time_error') and not context.get('time_error'):
        context['status'] = 200
        start_time_in_local_time = datetime.datetime.combine(date, start_time, time_difference)
        end_time_in_local_time = datetime.datetime.combine(date, end_time, time_difference)
        lesson.start_time = start_time_in_local_time.astimezone(UTC_ZONE) # store starting time in UTC
        lesson.end_time = end_time_in_local_time.astimezone(UTC_ZONE) # store ending time in UTC
        lesson.created_by = request.user
        lesson.save()
        context['schedule_success'] = "Your Lesson '" + lesson.name + "' Was Scheduled Successfully"
    return context
