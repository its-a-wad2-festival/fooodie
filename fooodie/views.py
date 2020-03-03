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
   
# Create your views here.
