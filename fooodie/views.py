from django.shortcuts import render, redirect
from django.http import HttpResponse


from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
    

context_dict={}

def home(request):
    response = render(request, 'fooodie/home.html', context=context_dict)
    return(response)

def about(request):
    response = render(request, 'fooodie/home.html', context=context_dict)
    return(response)

def user_signup_login(request):
    response = render(request, 'fooodie/home/html')
    return response

def user_logout(request):
    response = render(request, 'fooodie/home/html')
    return response

# May need to use multiple views for profiles; will try
# to figure out if view can used for both myprofile
# and other user profiles
def user_profile(request):
    response = render(request, 'fooodie/home/html')
    return response
   
# Create your views here.
