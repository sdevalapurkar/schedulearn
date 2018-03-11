from django.shortcuts import render
from django.http import HttpResponse
from .models import Relationships
from django.http import JsonResponse
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
        clients_tutors = Relationships.objects.filter(client=request.user)
        for tutor in clients_tutors:
            tutors.append([tutor.tutor.first_name, tutor.tutor.last_name, tutor.tutor.profile.id])

        
        return JsonResponse(tutors, safe=False)

        