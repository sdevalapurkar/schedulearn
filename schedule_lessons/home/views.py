from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login
from .forms import MyRegistrationForm


# Create your views here.

def load_home(request):
    if request.method == 'GET':
        form = MyRegistrationForm()
        return render(request, 'index.html', {'form': form, 'signup_errors': []})

def signup_view(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        # Check if signup information is valid
        if form.is_valid():
            form.save() # If it is, save the user in our database.
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            # Then authenticate this new user and log him in.
            new_user = authenticate(username=username, password=raw_password)

            new_user.profile.user_type = form.cleaned_data.get('tutor_or_student')
            new_user.profile.profile_pic = 'default/man.png'
            # Log in new user and take them home
            login(request, new_user)
            return redirect('dashboard')
        else:
            return render(request, 'index.html', {'form': form, 'signup_errors': form.errors.items(), 'login_errors': ''})
    else:
        form = MyRegistrationForm()
        return render(request, "index.html", {"form": form, 'signup_errors': [], 'login_error': ''})


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
