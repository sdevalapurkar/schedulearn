from django.shortcuts import render
from django.http import HttpResponse
from .models import Relationships, Events
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    
    return HttpResponse(status=404)

@login_required
def add_tutor(request):
    if request.method == 'POST':
        data = request.body
        return HttpResponse(status=200)

    return HttpResponse(status=404)


def get_tutors(request):
    if request.method == 'GET':
        tutors = []
        print (request.user)
        clients_tutors = Relationships.objects.filter(client=request.user)

        lee = User.objects.filter(username='leezeitz')
        for user in lee:
            print (user.first_name)

        print('\n')

        for tutor in clients_tutors:
            print(tutor.tutor.profile.id)
            print(tutor.tutor)
            print('full name: ' + tutor.tutor.get_full_name())
            tutors.append([tutor.tutor.first_name, tutor.tutor.last_name, tutor.tutor.profile.id])

        return JsonResponse(tutors, safe=False)

def get_events(request):
    if request.method == 'GET':
        event_list = []

        events = Events.objects.filter(client=request.user)

        for event in events:
            event_list.append({
                'name': event.name,
                'tutor_name': event.tutor.get_full_name(),
                'tutor_id': event.tutor.profile.id,
                'client_name': event.client.get_full_name(),
                'client_id': event.client.profile.id,
                'start_time': event.start_time,
                'end_time': event.end_time,
                'description': event.description
            })

        print (event_list)

    return JsonResponse(event_list, safe=False)

    return HttpResponse(status=404)