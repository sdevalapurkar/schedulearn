from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

def load_home(request):
    return render(request, 'index.html', {request: 'request'})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        passwordOne = request.POST.get('password1')
        passwordTwo = request.POST.get('password2')
        #User has send post request with information such as email, password
        #etc and they want to sing up.
        if passwordOne == passwordTwo:
            # The user enterered the password correctly.

            try:
                user = User.objects.get(username__iexact=username)
                return render(request, 'index.html', {'username_error': 'Username is already in use',  'email': email, 'username': username, 'firstName':firstName, 'lastName':lastName})
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email__iexact=email)
                    return render(request, 'index.html', {'email_error': 'Email is already in use','email': email, 'username': username, 'firstName':firstName, 'lastName':lastName})
                except User.DoesNotExist:
                    # If code gets here it means that email and username are not used and we can begin password validation.
                    try:
                        validate_password(passwordOne)
                    except ValidationError as password_errors:
                        return render(request, 'index.html', {'teacher_password_errors': password_errors,  'email': email, 'username': username, 'firstName':firstName, 'lastName':lastName})
                        #password validated, ready to put user in database.

                    user = User.objects.create_user(username, email=email, password=passwordOne)
                    user.first_name = firstName
                    user.last_name = lastName
                    user.profile.profile_pic = 'default/man.png'
                    user.save()
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('welcome')
        else:
            return render(request, 'index.html', {'password_error': 'Passwords do not match.', 'email': email, 'username': username, 'firstName':firstName, 'lastName':lastName})
    else:
        #User want to access homepage.
        return render(request, "index.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username'] # can be username or email
        password = request.POST['password']
        #check if email first.
        try:
            validate_email(username)
            # it's a valid email.
            try:
                user = User.objects.get(email__iexact=username) #searches the database if email exists, ignores case
            except User.DoesNotExist:
                return render(request, 'index.html', {'login_error': 'Invalid username/password combination'})
            valid_combination = user.check_password(password) # is a boolean, true if valid login.
            if valid_combination:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                if not user.profile.user_type:
                    return redirect('welcome')
                else:
                    return redirect('dashboard')
            else:
                return render(request, 'index.html', {'login_error': 'Invalid email/password combination'})
        except ValidationError:
            # it's a username.
            try:
                user = User.objects.get(username__iexact=username)
            except User.DoesNotExist:
                return render(request, 'index.html', {'login_error': 'Invalid username/password combination'})
            valid_combination = user.check_password(password)
            if valid_combination:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                if not user.profile.user_type:
                    return redirect('welcome')
                else:
                    return redirect('dashboard')
            else:
                return render(request, 'index.html', {'login_error': 'Invalid username/password combination'})

    else:
        return render(request, "index.html")

@login_required
def welcome(request):
    if request.method == 'POST':
        if request.POST.get('teacher_or_student') == 'teacher':
            request.user.profile.user_type = 'tutor'
            request.user.profile.profile_pic = 'default/man.png'
            request.user.save()
        else:
            request.user.profile.user_type = 'student'
            request.user.profile.profile_pic = 'default/man.png'
            request.user.save()
        return redirect('dashboard')
    else:
        if request.user.profile.user_type:
            return redirect('dashboard')
        else:
            return render(request, "welcome.html")
