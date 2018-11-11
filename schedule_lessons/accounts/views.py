'''This module contains the views that render the webpages when the user wants
    to go to a route.
'''
import base64
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.mail import get_connection
from django.core.mail.message import EmailMessage
from schedule_lessons.local_settings import (EMAIL_HOST, VERIFY_USER_EMAIL,
                                             FORGET_PASSWORD_EMAIL,
                                             EMAIL_HOST_PASSWORD, EMAIL_PORT)


def signup_view(request):
    '''This view handles the POST and GET request for signing a user up.'''
    context = {}
    if request.method == 'POST':
        context['email'] = request.POST.get('user_email')
        context['fullName'] = request.POST.get('user_name')
        context['passwordOne'] = request.POST.get('user_password1')
        context['passwordTwo'] = request.POST.get('user_password2')
        # User has send post request with information such as email, password
        # etc and they want to sign up.
        if not context['email']:
            context['email_missing_error'] = ('Please enter a valid email '
                                              'address.')
            return render(request, 'accounts/sign_up.html', context)
        if not context['fullName']:
            context['name_missing_error'] = 'Please enter your name.'
            return render(request, 'accounts/sign_up.html', context)

        if context['passwordOne'] == context['passwordTwo']:
            # The user enterered the password correctly.
            try:
                user = User.objects.get(email__iexact=context['email'])
                context['email_error'] = 'Email is already in use.'
                return render(request, 'accounts/sign_up.html', context)
            except User.DoesNotExist:
                # If code gets here it means that email is not used and we
                # can begin password validation.
                try:
                    validate_password(context['passwordOne'])
                except ValidationError as password_errors:
                    context['password_errors'] = password_errors
                    return render(request, 'accounts/sign_up.html', context)
                    #password validated, ready to put user in database.

                user = User.objects.create_user(context['email'],
                                                email=context['email'],
                                                password=context['passwordOne'])
                user.profile.fullName = context['fullName']
                context['fullName'] = context['fullName'].split()
                user.first_name = context['fullName'][0]
                if len(context['fullName']) > 1:
                    user.last_name = context['fullName'][-1]

                user.profile.profile_pic = 'default/man.png'
                user_id = user.profile.id
                user.profile.has_signed_up = True
                url = '{}accounts/verify_email/{}'.format(
                    request.build_absolute_uri('/'), user_id)
                with get_connection(
                        host=EMAIL_HOST,
                        port=EMAIL_PORT,
                        username=VERIFY_USER_EMAIL,
                        password=EMAIL_HOST_PASSWORD,
                        use_tls=True,
                ) as connection:
                    EmailMessage("Schedulearn - Verify Your Email Address",
                                 ("Click on the following link to verify your"
                                  "email address\n\n" + url),
                                 VERIFY_USER_EMAIL,
                                 [user.email],
                                 connection=connection).send()
                user.save()
                login(request, user,
                      backend='django.contrib.auth.backends.ModelBackend')
                return redirect('personalize')

        else:
            context['unmatching_password_error'] = 'Passwords do not match.'
    if not request.user.is_anonymous:
        # user is already signed in. so take him to the dashboard page.
        return redirect('agenda')
    return render(request, 'accounts/sign_up.html', context)


def login_view(request):
    '''This view handles the POST and GET request for logging a user in.'''
    context = {}
    if request.method == 'POST':
        context['email'] = request.POST.get('user_email')
        context['password'] = request.POST.get('user_password')
        #check if email first.
        try:
            #searches the database if email exists, ignores case
            user = User.objects.get(email__iexact=context['email'])
        except User.DoesNotExist:
            context['sign_in_error'] = 'Invalid username/password combination'
            return render(request, 'accounts/sign_in.html', context)

        if user.check_password(context['password']):
            login(request, user,
                  backend='django.contrib.auth.backends.ModelBackend')
            if not user.profile.has_signed_up:
                return redirect('personalize')
            return redirect('agenda')
        context['sign_in_error'] = 'Invalid username/password combination'
        return render(request, 'accounts/sign_in.html', context)

    if not request.user.is_anonymous:
        # user is already signed in. so take him to the agenda page.
        return redirect('agenda')
    if request.GET.get('reset', False):
        context['reset_password'] = ('Your password has been resetted. '
                                     'You can log in now.')
    return render(request, "accounts/sign_in.html", context)


@login_required
def personalize_view(request):
    '''This view handles the POST and GET request for the personalize webpage'''
    context = {
        'user': request.user
        }
    if request.method == 'POST':
        if request.POST.get('profile_pic', False):
            cropped_img = request.POST.get('profile_pic')
            img_format, imgstr = cropped_img.split(';base64,')
            ext = img_format.split('/')[-1]
            cropped_img = ContentFile(base64.b64decode(imgstr),
                                      name='temp.' + ext)
            request.user.profile.profile_pic = cropped_img
        if 'user-type' in request.POST:
            if request.POST.get('user-type') == 'tutor':
                request.user.profile.user_type = 'tutor'
            else:
                request.user.profile.user_type = 'student'
        if 'bio' in request.POST:
            request.user.profile.bio = request.POST.get('bio')

        request.user.save()
        return redirect('agenda')
    if request.method == 'GET':
        if request.user.profile.user_type:
            return redirect('agenda')
    return render(request, "accounts/personalize.html", context)

def forget_password(request):
    '''This view handles the POST and GET request for when a user forgets their
       password.
    '''
    context = {}
    if request.method == 'POST':
        context['user_email'] = request.POST.get('user_email')
        try:
            user = User.objects.get(email__iexact=context['user_email'])
        except User.DoesNotExist:
            context['email_error'] = "A user with this email doesn't exist."
            return render(request, 'accounts/forget_password.html', context)

        user_id = user.profile.id
        # building the reset password url
        url = '{}accounts/reset_password/{}'.format(
            request.build_absolute_uri('/'), user_id)
        with get_connection(
                host=EMAIL_HOST,
                port=EMAIL_PORT,
                username=FORGET_PASSWORD_EMAIL,
                password=EMAIL_HOST_PASSWORD,
                use_tls=True,
        ) as connection:
            EmailMessage("Schedulearn - Reset Your Password",
                         ("Go to this link to reset your password:\n\n"
                          + url + "\n\nIf you didn't request for this "
                          "password reset, then just ignore this email."),
                         FORGET_PASSWORD_EMAIL,
                         [context['user_email']],
                         connection=connection).send()
        context['check_email'] = 'Check your email for the reset link.'
    return render(request, 'accounts/forget_password.html', context)

def reset_password(request, user_id):
    '''This view handles the POST and GET request for when a user wants to
       reset their password.
    '''
    context = {}
    if request.method == 'POST':
        context['user_password1'] = request.POST.get('user_password1')
        context['user_password2'] = request.POST.get('user_password2')
        if context['user_password1'] == context['user_password2']:
            try:
                validate_password(context['user_password1'])
            except ValidationError as password_errors:
                context['weak_password_errors'] = password_errors
                return render(request, 'accounts/reset_password.html', context)
            user = User.objects.get(profile__id=user_id)
            user.set_password(context['user_password1'])
            user.save()
            response = redirect('login')
            response['Location'] += '?reset=true'
            return response
        else:
            context['unmatching_password_error'] = 'Passwords do not match.'
    return render(request, 'accounts/reset_password.html', context)


def verify_email(request, user_id):
    '''This view handles the GET request for verifying a user's email. If they
    go to this link, they'll automatically get verified if the id is valid in
    the url.
    '''
    context = {}
    try:
        user = User.objects.get(profile__id=user_id)
        user.profile.email_verified = True
        user.save()
        context['status'] = 'Your email address has been verified!'
    except User.DoesNotExist:
        context['status'] = 'This user does not exist.'
    return render(request, 'accounts/verify_email.html', context)
