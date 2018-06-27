from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
import base64
from django.core.files.base import ContentFile

def signup_view(request):
    if request.method == 'POST':
        email = request.POST['user_email']
        fullName = request.POST['user_name']
        passwordOne = request.POST['user_password1']
        passwordTwo = request.POST['user_password2']
        #User has send post request with information such as email, password
        #etc and they want to sing up.
        if passwordOne == passwordTwo:
            # The user enterered the password correctly.
            try:
                user = User.objects.get(email__iexact=email)
                return render(request, 'sign_up.html', {'email_error': 'Email is already in use.',  'email': email, 'fullName':fullName, 'password1':passwordOne, 'password2':passwordTwo})
            except User.DoesNotExist:
                # If code gets here it means that email is not used and we can begin password validation.
                try:
                    validate_password(passwordOne)
                except ValidationError as password_errors:
                    return render(request, 'sign_up.html', {'password_errors': password_errors,  'email': email, 'fullName':fullName, 'password1':passwordOne, 'password2':passwordTwo})
                    #password validated, ready to put user in database.

                user = User.objects.create_user(email, email=email, password=passwordOne)
                user.profile.fullName = fullName
                fullName = fullName.split()
                user.first_name = fullName[0]
                if len(fullName) > 1:
                    user.last_name = fullName[-1]

                user.profile.profile_pic = 'default/man.png'
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('personalize')

        else:
            return render(request, 'sign_up.html', {'unmatching_password_error': 'Passwords do not match.',  'email': email, 'fullName':fullName, 'password1':passwordOne, 'password2':passwordTwo})
    else:
        #User want to access homepage.
        return render(request, "sign_up.html")


def login_view(request):
    if request.method == 'POST':
        email = request.POST['user_email'] # can be username or email
        password = request.POST['user_password']
        #check if email first.
        try:
            user = User.objects.get(email__iexact=email) #searches the database if email exists, ignores case
        except User.DoesNotExist:
            return render(request, 'sign_in.html', {'sign_in_error': 'Invalid username/password combination'})

        valid_combination = user.check_password(password) # is a boolean, true if valid login.
        if valid_combination:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if not user.profile.user_type:
                return redirect('personalize')
            else:
                return redirect('dashboard')
        else:
            return render(request, 'sign_in.html', {'sign_in_error': 'Invalid email/password combination'})

    else:
        return render(request, "sign_in.html")

@login_required
def personalize_view(request):
    if request.method == 'POST':
        if 'profile_pic' in request.POST:
             cropped_img = request.POST['profile_pic']
             format, imgstr = cropped_img.split(';base64,')
             ext = format.split('/')[-1]
             cropped_img = ContentFile(base64.b64decode(imgstr), name='temp.' + ext) # You can save this as file instance.
             request.user.profile.profile_pic = cropped_img
        if 'user-type' in request.POST:
            if request.POST['user-type'] == 'tutor':
                request.user.profile.user_type = 'tutor'
            else:
                request.user.profile.user_type = 'student'

        request.user.save()
        return redirect('dashboard')
    else:
        if request.user.profile.user_type:
            return redirect('dashboard')
        else:
            return render(request, "personalize.html", {'user': request.user})
