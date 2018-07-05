from django.shortcuts import render

def load_home(request):
    print(request.user)
    print(request.user.is_anonymous)
    return render(request, 'home/homepage.html', {request: 'request'})
