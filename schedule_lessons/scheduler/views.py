from django.shortcuts import render
from django.http import HttpResponse
from .models import Relationships, Events
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    
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

@login_required
# Return list of tutors that have relationships with the client
def get_tutors(request):
    if request.method == 'GET':
        tutors = []
        clients_tutors = Relationships.objects.filter(client=request.user)

        for tutor in clients_tutors:
            tutors.append([tutor.tutor.first_name, tutor.tutor.last_name, tutor.tutor.profile.id])

        return JsonResponse(tutors, safe=False)

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