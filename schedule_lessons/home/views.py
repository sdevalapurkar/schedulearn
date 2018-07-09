from django.shortcuts import render

def load_home(request):
    return render(request, 'home/homepage.html', {request: 'request'})
