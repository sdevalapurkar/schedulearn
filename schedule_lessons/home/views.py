from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def load_home(request):
    return render(request, 'index.html')

def signup_view(request):
    if request.method == 'POST':
        #User has send post request with information such as email, password
        #etc and they want to sing up.
        if request.POST.get('teacher_or_student') == 'teacher': #signing up as a tutor
            if request.POST.get('password1') == request.POST.get('password2'):
                # The user enterered the password correctly.
                username = request.POST.get('username')
                email = request.POST.get('email')
                try:
                    user = User.objects.get(username__iexact=username)
                    return render(request, 'index.html', {'teacher_username_error': 'Username is already in use',  'teacher_email': request.POST.get('email'), 'teacher_username': request.POST.get('username'), 'teacher_firstName':request.POST.get('firstName'), 'teacher_lastName':request.POST.get('lastName')})
                except User.DoesNotExist:
                    try:
                        user = User.objects.get(email__iexact=email)
                        return render(request, 'index.html', {'teacher_email_error': 'Email is already in use','teacher_email': request.POST.get('email'), 'teacher_username': request.POST.get('username'), 'teacher_firstName':request.POST.get('firstName'), 'teacher_lastName':request.POST.get('lastName')})
                    except User.DoesNotExist:
                        # If code gets here it means that email and username are not used and we can begin password validation.
                        try:
                            validate_password(request.POST.get('password1'))
                        except ValidationError as password_errors:
                            return render(request, 'index.html', {'teacher_password_errors': password_errors,  'teacher_email': request.POST.get('email'), 'teacher_username': request.POST.get('username'), 'teacher_firstName':request.POST.get('firstName'), 'teacher_lastName':request.POST.get('lastName')})
                        #password validated, ready to put user in database.

                        user = User.objects.create_user(username, email=request.POST['email'], password=request.POST['password1'])
                        user.first_name = request.POST['firstName']
                        user.last_name = request.POST['lastName']
                        user.profile.profile_pic = 'default/man.png'
                        user.profile.user_type = request.POST.get('teacher_or_student')
                        user.save()
                        login(request, user)
                        return redirect('dashboard')
            else:
                return render(request, 'index.html', {'teacher_password_error': 'Passwords do not match.', 'teacher_email': request.POST.get('email'), 'teacher_username': request.POST.get('username'), 'teacher_firstName':request.POST.get('firstName'), 'teacher_lastName':request.POST.get('lastName')})

        else: #signing up as a student
            if request.POST.get('password1') == request.POST.get('password2'):
                # The user enterered the password correctly.
                username = request.POST.get('username')
                email = request.POST.get('email')
                try:
                    user = User.objects.get(username__iexact=username)
                    return render(request, 'index.html', {'student_username_error': 'Username is already in use',  'student_email': request.POST.get('email'), 'username': request.POST.get('username'), 'firstName':request.POST.get('firstName'), 'lastName':request.POST.get('lastName')})
                except User.DoesNotExist:
                    try:
                        user = User.objects.get(email__iexact=email)
                        return render(request, 'index.html', {'student_email_error': 'Email is already in use',  'email': request.POST.get('email'), 'username': request.POST.get('username'), 'firstName':request.POST.get('firstName'), 'lastName':request.POST.get('lastName')})
                    except User.DoesNotExist:
                        # If code gets here it means that email and username are not used and we can begin password validation.
                        try:
                            validate_password(request.POST.get('password1'))
                        except ValidationError as password_errors:
                            return render(request, 'index.html', {'student_password_errors': password_errors, 'teacher_email': request.POST.get('email'), 'teacher_username': request.POST.get('username'), 'teacher_firstName':request.POST.get('firstName'), 'teacher_lastName':request.POST.get('lastName')})
                        #password validated, ready to put user in database.

                        user = User.objects.create_user(username, email=request.POST['email'], password=request.POST['password1'])
                        user.first_name = request.POST['firstName']
                        user.last_name = request.POST['lastName']
                        user.profile.profile_pic = 'default/man.png'
                        user.profile.user_type = request.POST.get('teacher_or_student')
                        user.save()
                        login(request, user)
                        return redirect('dashboard')
            else:
                return render(request, 'index.html', {'student_password_error': 'Passwords do not match.', 'teacher_email': request.POST.get('email'), 'teacher_username': request.POST.get('username'), 'teacher_firstName':request.POST.get('firstName'), 'teacher_lastName':request.POST.get('lastName')})





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
            user = User.objects.get(email__iexact=username) #searches the database if email exists, ignores case
            valid_combination = user.check_password(password) # is a boolean, true if valid login.
            if valid_combination:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'index.html', {'login_error': 'Invalid email/password combination'})
        except ValidationError:
            # it's a username.
            user = User.objects.get(username__iexact=username)
            valid_combination = user.check_password(password)
            if valid_combination:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'index.html', {'login_error': 'Invalid username/password combination'})

    else:
        return render(request, "index.html")
