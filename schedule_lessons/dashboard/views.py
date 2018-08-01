from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from .models import Relationship, Lesson
from accounts.models import Availability
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import get_connection
from django.core.mail.message import EmailMessage
import base64
from django.core.files.base import ContentFile
from schedule_lessons.local_settings import *

# returns scheduler information for scheduler tab for the user.
@login_required
def agenda(request):
    if request.method == 'GET':
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
                    'location': lesson.location,
                    'tutor_name': lesson.tutor.get_full_name(),
                    'tutor_id': lesson.tutor.profile.id,
                    'student_name': lesson.student.get_full_name(),
                    'student_id': lesson.student.profile.id,
                    'month': lesson.start_time.strftime('%b'),
                    'day': lesson.start_time.strftime('%a'),
                    'month_day': lesson.start_time.strftime('%d'),
                    'year': lesson.start_time.strftime('%Y'),
                    'start_time': lesson.start_time.strftime('%I:%M %p'),
                    'end_time': lesson.end_time.strftime('%I:%M %p'),
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
        profile_user = User.objects.get(profile__id=user_id) # get the user to which the profile belongs
        availabilities = return_availabilities(request, user_id)

        if not request.user.is_anonymous:
            if request.user.profile.user_type == 'tutor':
                if relationship_exists(profile_user, request.user):
                    remove_student_url = request.build_absolute_uri('/') + 'dashboard/remove_student/' + str(user_id)
                    return render(request, 'dashboard/public_profile.html', {'profile_user': profile_user, 'availabilities': availabilities, 'rel_exists': True, 'remove_student_url':remove_student_url})
                else:
                    add_student_url = request.build_absolute_uri('/') + 'dashboard/add_student/' + str(user_id)
                    return render(request, 'dashboard/public_profile.html', {'profile_user': profile_user, 'availabilities': availabilities, 'add_student_url': add_student_url})
            elif request.user.profile.user_type == 'student':
                if relationship_exists(request.user, profile_user):
                    remove_tutor_url = request.build_absolute_uri('/') + 'dashboard/remove_tutor/' + str(user_id)
                    return render(request, 'dashboard/public_profile.html', {'profile_user': profile_user, 'availabilities': availabilities, 'rel_exists': True, 'remove_tutor_url':remove_tutor_url})
                else:
                    add_tutor_url = request.build_absolute_uri('/') + 'dashboard/add_tutor/' + str(user_id)
                    return render(request, 'dashboard/public_profile.html', {'profile_user': profile_user, 'availabilities': availabilities, 'add_tutor_url': add_tutor_url})
        else:
            return render(request, 'dashboard/public_profile.html', {'profile_user': profile_user, 'availabilities': availabilities})

    except Exception as e:
        return HttpResponse(status=404) # replace with return of the error 404 page after it's made.

@login_required
def add_student(request, student_id):
    student_profile = User.objects.get(profile__id=student_id)
    new_rel = Relationship(student=student_profile, tutor=request.user)
    new_rel.save()
    return public_profile(request, student_id)

@login_required
def remove_student(request, student_id):
    student_profile = User.objects.get(profile__id=student_id)
    old_rel = Relationship.objects.get(student=student_profile, tutor=request.user)
    old_rel.delete()
    return public_profile(request, student_id)

@login_required
def add_tutor(request, tutor_id):
    tutor_profile = User.objects.get(profile__id=tutor_id)
    new_rel = Relationship(student=request.user, tutor=tutor_profile)
    new_rel.save()
    return public_profile(request, tutor_id)

@login_required
def remove_tutor(request, tutor_id):
    tutor_profile = User.objects.get(profile__id=tutor_id)
    old_rel = Relationship.objects.get(student=request.user, tutor=tutor_profile)
    old_rel.delete()
    return public_profile(request, tutor_id)

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
    person_to_schedule_with = User.objects.get(profile__id=user_id)
    context = {'person_to_schedule_with': person_to_schedule_with, 'availabilities': return_availabilities(request, user_id)}
    if request.method == 'POST':
        new_lesson = Lesson()
        context = error_check_and_save_lesson(request, new_lesson, context)
        context['schedule_success'] = "Your Lesson '" + new_lesson.name + "' Was Scheduled Successfully"
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
        'person_to_schedule_with': User.objects.get(profile__id=lesson_to_reschedule.student.profile.id) if request.user.profile.user_type == 'tutor' else User.objects.get(profile__id=lesson_to_reschedule.tutor.profile.id),
    }
    if request.method == 'POST':
        context = error_check_and_save_lesson(request, lesson_to_reschedule, context)
        if context.get('name_error') or context.get('location_error') or context.get('date_error') or context.get('starting_time_error') or context.get('ending_time_error'):
            return render(request, 'dashboard/schedule_lesson.html', context)
        return redirect('agenda')
    else:
        if lesson_to_reschedule and (lesson_to_reschedule.tutor == request.user or lesson_to_reschedule.student == request.user):
            context['availabilities'] = return_availabilities(request, context['person_to_schedule_with'].profile.id)
            context['lesson_to_reschedule'] = {
                'name': lesson_to_reschedule.name,
                'location': lesson_to_reschedule.location,
                'date': lesson_to_reschedule.end_time.strftime('%m/%d/%Y'),
                'start_time': lesson_to_reschedule.start_time.strftime('%I:%M %p'),
                'end_time': lesson_to_reschedule.end_time.strftime('%I:%M %p'),
            }
            return render(request, 'dashboard/schedule_lesson.html', context)
        else:
            return HttpResponse(status=404)

# viewing MY profile will be different than viewing somebody else's profile, hence
# a new view template and url will be set up for the feature of viewing someone else's profile.
@login_required
def my_profile(request):
    reset_email = request.GET.get('reset_email', False)
    availabilities = return_availabilities(request, request.user.profile.id)
    if reset_email:
        return render(request, 'dashboard/my_profile.html', {'user': request.user, 'availabilities': availabilities, 'changed_email': True})
    else:
        return render(request, 'dashboard/my_profile.html', {'user': request.user, 'availabilities': availabilities})

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
    context = {'availabilities': return_availabilities(request, request.user.profile.id)}
    if request.method == 'POST':
        try:
            existing_availabity = Availability.objects.get(profile__id=request.user.profile.id, day=request.POST['day'])
            if not request.POST['startingTime'] or not request.POST['endingTime']:
                return check_for_empty_times(request, context)
            else:
                existing_availabity.start_time = datetime.datetime.strptime(request.POST['startingTime'], '%I:%M %p')
                existing_availabity.end_time = datetime.datetime.strptime(request.POST['endingTime'], '%I:%M %p')
                existing_availabity.save()
                return redirect('edit_availability')
        except:
            new_availability = Availability()
            new_availability.profile = request.user.profile
            new_availability.day = request.POST['day']
            if not request.POST['startingTime'] or not request.POST['endingTime']:
                return check_for_empty_times(request, context)
            else:
                new_availability.start_time = datetime.datetime.strptime(request.POST['startingTime'], '%I:%M %p')
                new_availability.end_time = datetime.datetime.strptime(request.POST['endingTime'], '%I:%M %p')
                new_availability.save()
                return redirect('edit_availability')
    else:
        return render(request, 'dashboard/edit_availability.html', context)

@login_required
def delete_availability(request, day):
    delete_day = Availability.objects.get(profile__id=request.user.profile.id, day__iexact=day)
    delete_day.delete()
    return redirect('edit_availability')

# Functions for the views

def relationship_exists(student, tutor):
    try:
        Relationship.objects.get(student=student, tutor=tutor)
        return True
    except:
        return False

def check_for_empty_times(request, context):
    if not request.POST['startingTime']:
        context['starting_time_error'] = True
    if not request.POST['endingTime']:
        context['ending_time_error'] = True

    if context.get('ending_time_error') or context.get('starting_time_error'):
        return render(request, 'dashboard/edit_availability.html', context)

def return_availabilities(request, profile_id):
    availabilities = []
    days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in days_of_the_week:
        availabilities_db = Availability.objects.filter(profile__id=profile_id, day=day)
        if availabilities_db:
            availabilities.append({
                'day': availabilities_db[0].day,
                'start_time': availabilities_db[0].start_time.strftime('%I:%M %p'),
                'end_time': availabilities_db[0].end_time.strftime('%I:%M %p') })
        else:
            availabilities.append({
                'day': day,
                'unavailable': True })

    # availabilities.sort(key=lambda v: days_of_the_week.index(v['day'])) # sorts the availabilities by the day of the week.
    return availabilities

def error_check_and_save_lesson(request, lesson, context):
    if not request.POST['name']:
        context['name_error'] = True
    else:
        lesson.name = request.POST['name']
    if not request.POST['location']:
        context['location_error'] = True
    else:
        lesson.location = request.POST['location']
    if not request.POST['date']:
        context['date_error'] = True
    else:
        date = datetime.datetime.strptime(request.POST['date'], '%m/%d/%Y').date() # a date object.
    if not request.POST['startingTime']:
        context['starting_time_error'] = True
    else:
        start_time = datetime.datetime.strptime(request.POST['startingTime'], '%I:%M %p').time() # a time object
    if not request.POST['endingTime']:
        context['ending_time_error'] = True
    else:
        end_time = datetime.datetime.strptime(request.POST['endingTime'], '%I:%M %p').time()

    lesson.tutor = request.user if request.user.profile.user_type == 'tutor' else context['person_to_schedule_with']
    lesson.student = request.user if request.user.profile.user_type == 'student' else context['person_to_schedule_with']

    if not context.get('name_error') and not context.get('location_error') and not context.get('date_error') and not context.get('starting_time_error') and not context.get('ending_time_error'):
        lesson.start_time = datetime.datetime.combine(date, start_time)
        lesson.end_time = datetime.datetime.combine(date, end_time)
        lesson.created_by = request.user
        lesson.save()
    return context
