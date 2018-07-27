from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
import base64
from django.core.files.base import ContentFile
from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
from schedule_lessons.local_settings import *

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
                return render(request, 'accounts/sign_up.html', {'email_error': 'Email is already in use.',  'email': email, 'fullName':fullName, 'password1':passwordOne, 'password2':passwordTwo})
            except User.DoesNotExist:
                # If code gets here it means that email is not used and we can begin password validation.
                try:
                    validate_password(passwordOne)
                except ValidationError as password_errors:
                    return render(request, 'accounts/sign_up.html', {'password_errors': password_errors,  'email': email, 'fullName':fullName, 'password1':passwordOne, 'password2':passwordTwo})
                    #password validated, ready to put user in database.

                user = User.objects.create_user(email, email=email, password=passwordOne)
                user.profile.fullName = fullName
                fullName = fullName.split()
                user.first_name = fullName[0]
                if len(fullName) > 1:
                    user.last_name = fullName[-1]

                user.profile.profile_pic = 'default/man.png'
                id = user.profile.id
                user.profile.has_signed_up = True
                url = request.build_absolute_uri('/') + "accounts/verify_email/" + str(id)
                with get_connection(
                    host=EMAIL_HOST,
                    port=EMAIL_PORT,
                    username=VERIFY_USER_EMAIL,
                    password=EMAIL_HOST_PASSWORD,
                    use_tls=True,
                ) as connection:
                    EmailMessage("Schedulearn - Verify Your Email Address",
                                 "Click on the following link to verify your email address\n\n" + url,
                                 VERIFY_USER_EMAIL,
                                 [user.email],
                                 connection=connection).send()
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('personalize')

        else:
            return render(request, 'accounts/sign_up.html', {'unmatching_password_error': 'Passwords do not match.',  'email': email, 'fullName':fullName, 'password1':passwordOne, 'password2':passwordTwo})
    else:
        #User want to access homepage.
        if request.user.is_anonymous:
            # if the user is not logged in, just send him to the sign up page.
            return render(request, "accounts/sign_up.html")
        else:
            # user is already signed in. so take him to the dashboard page.
            return redirect('agenda')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['user_email'] # can be username or email
        password = request.POST['user_password']
        #check if email first.
        try:
            user = User.objects.get(email__iexact=email) #searches the database if email exists, ignores case
        except User.DoesNotExist:
            return render(request, 'accounts/sign_in.html', {'sign_in_error': 'Invalid username/password combination', 'email': email, 'password': password})

        valid_combination = user.check_password(password) # is a boolean, true if valid login.
        if valid_combination:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if not user.profile.user_type:
                return redirect('personalize')
            else:
                return redirect('agenda')
        else:
            return render(request, 'accounts/sign_in.html', {'sign_in_error': 'Invalid email/password combination', 'email': email, 'password': password})

    else:
        reset = request.GET.get('reset', False)
        if reset:
            return render(request, "accounts/sign_in.html", {'reset_password': 'Your password has been resetted. You can log in now.'})
        else:
            if request.user.is_anonymous:
                # if the user is not logged in, just send him to the sign up page.
                return render(request, "accounts/sign_in.html")
            else:
                # user is already signed in. so take him to the agenda page.
                return redirect('agenda')


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
        if 'bio' in request.POST:
            request.user.profile.bio = request.POST['bio']

        request.user.save()
        return redirect('agenda')
    else:
        if request.user.profile.user_type:
            return redirect('agenda')
        else:
            return render(request, "accounts/personalize.html", {'user': request.user})

def forget_password(request):
    if request.method == 'POST':
        user_email = request.POST['user_email']
        try:
            user = User.objects.get(email__iexact=user_email)
            id = user.profile.id
            # building the reset password url
            url = request.build_absolute_uri('/') + "accounts/reset_password/" + str(id)
            # example url: http://127.0.0.1:8000/accounts/reset_password/94c662bf-3542-4090-b776-29bebb1112f5

            with get_connection(
                host=EMAIL_HOST,
                port=EMAIL_PORT,
                username=FORGET_PASSWORD_EMAIL,
                password=EMAIL_HOST_PASSWORD,
                use_tls=True,
            ) as connection:
                EmailMessage("Schedulearn - Reset Your Password",
                             "Go to the following link to reset your password:\n\n" + url + "\n\nIf you didn't request for this password reset, then just ignore this email.",
                             FORGET_PASSWORD_EMAIL,
                             [user_email],
                             connection=connection).send()
        except Exception as e:
            return render(request, 'accounts/forget_password.html', {'email_error': "A user with this email doesn't exist.", 'user_email': user_email})
        return render(request, 'accounts/forget_password.html', {'check_email':'Check your email for the reset link.', 'user_email': user_email})
    else:
        return render(request, 'accounts/forget_password.html')

def reset_password(request, id):
    if request.method == 'POST':
        password1 = request.POST['user_password1']
        password2 = request.POST['user_password2']
        if password1 == password2:
            try:
                validate_password(password1)
            except ValidationError as password_errors:
                return(request, 'accounts/reset_password.html', {'weak_password_errors': password_errors, 'user_password1': password1, 'user_password2': password2})
            user = User.objects.get(profile__id=id)
            user.set_password(password1)
            user.save()
            response = redirect('login')
            response['Location'] += '?reset=true'
            return response
        else:
            return render(request, 'accounts/reset_password.html', {'unmatching_password_error': 'Passwords do not match.', 'user_password1': password1, 'user_password2': password2})
    return render(request, 'accounts/reset_password.html')


def verify_email(request, id):
    try:
        user = User.objects.get(profile__id=id)
    except:
        return render(request, 'accounts/verify_email.html', {'status': 'This user does not exist.'})
    user.profile.email_verified = True
    user.save()
    return render(request, 'accounts/verify_email.html', {'status': 'Your email address has been verified!'})
