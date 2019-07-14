'''This module contains the views that render the webpages when the user wants
    to go to a route.
'''
import base64
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile

from accounts.models import Preference


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
                Preference.create(request.user,
                    "Force Lesson Timings To Be Within Your Availablity",
                    "Choose if you want lessons scheduled with you to be"
                    " only within your availablity timings.",
                    True)
                Preference.create(request.user,
                    "Allow Students To Schedule Lessons",
                    "Choose if you want students to be able to make"
                    " lesson requests with you.",
                    False)
            else:
                request.user.profile.user_type = 'student'
                Preference.create(request.user,
                    "Force Lesson Timings To Be Within Your Availablity",
                    "Choose if you want lessons scheduled with you to be"
                    " only within your availablity timings.",
                    True)
        if 'bio' in request.POST:
            request.user.profile.bio = request.POST.get('bio')
        request.user.save()
        return redirect('agenda')
    if request.method == 'GET':
        if request.user.profile.user_type:
            return redirect('agenda')
        else:
            return render(request, "account/personalize.html", context)
