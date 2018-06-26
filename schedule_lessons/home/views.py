from django.shortcuts import render

def load_home(request):
    return render(request, 'homepage.html', {request: 'request'})
