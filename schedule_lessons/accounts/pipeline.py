from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
from schedule_lessons.local_settings import *

# this checks if there is already a user with the gmail address that the user is trying to sign up with
def check_duplicate_email(request, backend, user, response, *args, **kwargs):
    email = response['emails'][0]['value']
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        contains_social_authentication = user.social_auth.filter(provider='google-oauth2')
        if contains_social_authentication:
            return
        else:
            return render(request, 'sign_up.html', {'sign_up_google_email_error': 'Email is already in use, sign in manually or use another google account'})

    return

def load_welcome(request, backend, user, response, *args, **kwargs):
    if not user.profile.user_type:
        user.profile.profile_pic = 'default/man.png'
        id = user.profile.id
        url = request.build_absolute_uri('/') + "accounts/verify_email/" + str(id)
        if not user.profile.has_signed_up:
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
        user.profile.has_signed_up = True
        user.save()
        login(request, user, backend='social_core.backends.google.GoogleOAuth2')
        return redirect('personalize')
    else:
        return
    return
