from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate

# Create your views here.

def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'signup/signup.html', {'form': form})
    return HttpResponse(status=404)

# Create new Tutor
def signup_tutor(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'signup/signup.html', {'form': form})
        
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        print (request.POST)
        if form.is_valid():
            # Create the user
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            # Authenticate new user and add them to tutor group
            new_user = authenticate(username=username, password=raw_password)
            Group.objects.get(name='tutor').user_set.add(new_user)

            # Log in new user and take them home
            login(request, user)
            return redirect('home')     

    return HttpResponse(status=404)


# Create new Client
def signup_client(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'signup/signup.html', {'form': form})
        
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        print (request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
       
            new_user = authenticate(username=username, password=raw_password)
            Group.objects.get(name='client').user_set.add(new_user)

            login(request, user)
            return redirect('home')     

    return HttpResponse(status=404)