from django.shortcuts import render
import json
import datetime
from django.http import HttpResponse
from .models import Relationships, Events
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    if request.method == 'GET':
        user_type = request.user.profile.user_type
        return render(request, 'index.html', {'user_type': user_type})
    
    return HttpResponse(status=404)


# Create a relationship between the client and a tutor
@login_required
def add_tutor(request):
    if request.method == 'POST':
        tutor_id = request.body['tutor_id']
        try:
            Relationships(client=request.user, tutor=User.objects.get(profile__id=tutor_id))
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
                response.append([tutor.tutor.first_name, tutor.tutor.last_name, tutor.tutor.profile.id])
        else:
            for tutor in clients_tutors:
                response.append([tutor.client.first_name, tutor.client.last_name, tutor.client.profile.id])

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
            start_time = data.get('startDate')

            end_time = data.get('endDate')
            description = data.get('lessonDescription')
            tutor = User.objects.get(profile__id=data.get('tutorID'))

            event = Events(name=name, tutor=tutor, start_time = start_time, end_time = end_time, description=description, client=request.user)
            event.save()
            return HttpResponse(status=200)
        except Exception as e:
            print (str(e))
            return HttpResponse(status=404)
    return HttpResponse(status=404)


def get_availability(request, tutor_id):
    if request.method == 'GET':
        tutor = User.objects.get(profile__id=tutor_id)
        availability = tutor.profile.availability
        return render(request, 'Schedulerpage.html', {'availability': availability})
    return HttpResponse(status=404)


def set_availability(request):
    if request.method == 'POST':
        data = request.body
        try:
            tutor = User.objects.get(profile__id=data['id'])
            tutor.profile.availability = data['data']
            tutor.save()
            return HttpResponse(status=200)
        except Exception as e:
            print(str(e))

    return HttpResponse(status=404)
