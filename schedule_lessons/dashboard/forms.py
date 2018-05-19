from django import forms
from django.contrib.auth.models import User
from home.models import Profile

class NameForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ('profile_pic',)
