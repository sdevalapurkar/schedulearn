'''This module contains the view that renders the homepage.'''
from django.shortcuts import render

def load_home(request):
    '''This view serves the homepage to the user.'''
    return render(request, 'home/homepage.html', {request: 'request'})

def load_privacy_policy(request):
    '''This view serves the privacy policy page to the user.'''
    return render(request, 'home/privacy_policy.html')
