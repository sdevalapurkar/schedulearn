from django.shortcuts import render
import json
import datetime
from django.http import HttpResponse
from .models import Relationships, Events
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

# Create your views here.
@login_required
def home(request):
    if request.method == 'GET':
        user_type = request.user.profile.user_type

        pending_event_list = []
        event_list = []
        if user_type == 'client':
            events = Events.objects.filter(client=request.user)
        else:
            events = Events.objects.filter(tutor=request.user)
        for event in events:
            try:
                data = {
                    'id': event.id,
                    'name': event.name,
                    'tutor_name': event.tutor.get_full_name(),
                    'tutor_id': event.tutor.profile.id,
                    'tutor_username': event.tutor.username,
                    'client_name': event.client.get_full_name(),
                    'client_id': event.client.profile.id,
                    'client_username': event.client.username,
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
                print(str(e))
        return render(request, 'index.html', {'user_type': user_type, 'events': event_list, 'pending_events': pending_event_list})
    
    return HttpResponse(status=404)


# Create a relationship between the client and a tutor
@login_required
def add_tutor(request):
    if request.method == 'POST':
        tutor_id = request.POST.get('tutor_id')
        try:
            try:
                existing_rel = Relationships.objects.get(client=request.user, tutor=User.objects.get(profile__id=tutor_id))
                return HttpResponse(status=200)

            except Exception as e:
                print(str(e))
                new_rel = Relationships(client=request.user, tutor=User.objects.get(profile__id=tutor_id))
                new_rel.save()
                return HttpResponse(status=200)
        except Exception as e:
            print (str(e))
            return HttpResponse(status=404)
    return HttpResponse(status=404)


# Return list of tutors that have relationships with the client
@login_required
def get_tutors(request):
    if request.method == 'GET':
        response = []
        clients_tutors = Relationships.objects.filter(client=request.user)
        if request.user.profile.user_type == 'client':
            for tutor in clients_tutors:
                response.append([tutor.tutor.first_name, tutor.tutor.last_name, tutor.tutor.profile.id, tutor.tutor.email])
        else:
            for tutor in clients_tutors:
                response.append([tutor.client.first_name, tutor.client.last_name, tutor.client.profile.id, tutor.tutor.email])

        return JsonResponse(response, safe=False)


@login_required
def get_events(request):
    if request.method == 'GET':
        event_list = []

        events = Events.objects.filter(client=request.user)

        for event in events:
            event_list.append({
                'name': event.name,
                'tutor_name': event.tutor.get_full_name(),
                'tutor_id': event.tutor.profile.id,
                'tutor_username': event.tutor.username,
                'client_name': event.client.get_full_name(),
                'client_id': event.client.profile.id,
                'client_username': event.client.username,
                'start_time': event.start_time,
                'end_time': event.end_time,
                'description': event.description
            })
        return JsonResponse(event_list, safe=False)
    return HttpResponse(status=404)


@login_required
def set_event(request):
    if request.method == 'POST':   
        data = request.POST
        try:
            name = data.get('lessonName')
            start_time = datetime.datetime.strptime(data.get('startDate'), '%m/%d/%Y %I:%M %p')

            end_time = datetime.datetime.strptime(data.get('endDate'), '%m/%d/%Y %I:%M %p')

            description = data.get('lessonDescription')
            tutor = User.objects.get(profile__id=data.get('tutorID'))

            event = Events(name=name, tutor=tutor, start_time = start_time, end_time = end_time, description=description, client=request.user)
            event.save()

            send_mail(
                'Schedulearn: Lesson scheduled!',
                'Student: ' + request.user.first_name + ' ' + request.user.last_name +  '. ' + str(name) + ': ' + str(description) + '. ' + 'Start time: ' + str(start_time) + '. End time: ' + str(end_time) + '. Please visit Schedulearn to confirm this lesson.',
                'schedulearn@schedulearn.com',
                [tutor.email],
                fail_silently=False,
            )

            return HttpResponse(status=200)
        except Exception as e:
            print (str(e))
            return HttpResponse(status=404)
    return HttpResponse(status=404)


def get_availability(request, tutor_id):
    if request.method == 'GET':
        tutor = User.objects.get(profile__id=tutor_id)
        availability = tutor.profile.availability
        if tutor.profile.availability is not None:
            availability = json.loads(tutor.profile.availability.replace("'", '"'))
        if availability == {} or availability == '{}':
            availability = None
        
        return render(request, 'Schedulerpage.html', {'availability': availability, 'user_full_name': tutor.get_full_name()})
    return HttpResponse(status=404)

def set_availability(request):
    if request.method == 'POST':
        data = request.body
        try:
            tutor = User.objects.get(profile__id=data.get('id'))
            tutor.profile.availability = data.get('data')
            tutor.save()
            return HttpResponse(status=200)
        except Exception as e:
            print(str(e))

    return HttpResponse(status=404)


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
            print (str(e))

    return HttpResponse(status=404)

def my_profile(request):
    if request.method == 'GET':
        return render(request, 'my_profile.html', {'user': request.user})
    return HttpResponse(status=404)

def user_type(request):
    if request.method == 'GET':
        return JsonResponse({'user_type': request.user.profile.user_type, 'id': request.user.profile.id})
    return HttpResponse(status=404)

def confirm_lesson(request):
    if request.method == 'POST':
        event_id = request.POST.get('id')
        event = Events.objects.get(id=event_id)
        event.pending = False
        event.save()
        return HttpResponse(status=200)
    return HttpResponse(status=404)


def decline_lesson(request):
    if request.method == 'POST':
        event_id = request.POST.get('id')
        Events.objects.get(id=event_id).delete()
        return HttpResponse(status=200)
    return HttpResponse(status=404)