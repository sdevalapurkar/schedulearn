from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login

def load_home(request):
    return render(request, 'index.html')

def signup_view(request):
    if request.method == 'POST':
        #User has send post request with information such as email, password
        #etc and they want to sing up.
        return render(request, "index.html")
    else:
        #User want to access homepage.
        return render(request, "index.html")


def login_view(request):
    form = MyRegistrationForm()
    if request.method == 'POST':
        username = request.POST['u']
        password = request.POST['p']
        caseSensitiveUsername = username

        try:
            findUser = User._default_manager.get(username__iexact=username)
        except User.DoesNotExist:
            findUser = None

        if findUser is not None:
            caseSensitiveUsername = findUser


        user = authenticate(username=caseSensitiveUsername, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            login_error = "Invalid username/password combination. Please try again."
            return render(request, "index.html", {"form": form, 'signup_errors': [], 'login_error': login_error})

    else:
        return render(request, "index.html", {"form": form, 'signup_errors': [], 'login_error': ''})
