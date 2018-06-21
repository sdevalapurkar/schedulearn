from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login

# this checks if there is already a user with the gmail address that the user is trying to sign up with
def check_duplicate_email(request, backend, user, response, *args, **kwargs):
    email = response['emails'][0]['value']
    print("Does duplicate user with email exist? ", User.objects.filter(email=email).exists())
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        contains_social_authentication = user.social_auth.filter(provider='google-oauth2')
        if contains_social_authentication:
            return
        else:
            return render(request, 'index.html', {'sign_up_google_email_error': 'Email is already in use, sign in manually or use another google account'})

    return

def load_welcome(request, backend, user, response, *args, **kwargs):
    if not user.profile.user_type:
        login(request, user, backend='social_core.backends.google.GoogleOAuth2')
        return render(request, 'welcome.html')
    else:
        return
    return
