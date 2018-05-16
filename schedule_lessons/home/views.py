from django.shortcuts import render

# Create your views here.

def load_home(request):
    return render(request, 'index.html')
