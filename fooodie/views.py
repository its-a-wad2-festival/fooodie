from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.conf import settings
from fooodie.models import Photo, UserProfile
from fooodie.forms import UserForm, UserProfileForm
import os

def home(request):
    context_dict = {}

##    #Ordering all photos randomly, picking first two
##    pics_to_choose = Photo.objects.order_by(?)[:1]
##    context_dict['pics_to_choose'] = pics_to_choose
##
##    #Will change this to use the same QuerySet eventually, to avoid double
##    #search and having the same picture be both a voting pic and random pic
##    random_pics = Photo.objects.order_by(?)[:3]
##    context_dict['random_pics'] = random_pics

    #Above will definitely work, this SHOULD work
    pics = Photo.objects.order_by('?')

    pics_to_choose = pics[:2]
    context_dict['pics_to_choose'] = pics_to_choose

    random_pics = pics[:4]
    context_dict['random_pics'] = random_pics

    response = render(request, 'fooodie/home.html', context = context_dict)
    return(response)

def about(request):
    context_dict = {}
    response = render(request, 'fooodie/about.html')
    return(response)

def leaderboard(request):
    context_dict = {}
    top_pics = Photo.objects.order_by('-votes')[:3] #Top 3
    context_dict['top_pics'] = top_pics

    top_profiles = UserProfile.objects.order_by('-totalVotes')[:8] #Top 8
    context_dict['top_profiles'] = top_profiles

    response = render(request, 'fooodie/leaderboard.html', context = context_dict)
    return(response)

def user_signup_login(request):
    context_dict = {}

    response = render(request, 'fooodie/home.html')
    return response

#Will focus on the registration/login logic first, implement into a single view later
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            print('user id: '+str(user.id))

            #Creating the user's folder so we can put the profile pic into it
            folder_path = os.path.join(settings.MEDIA_DIR, str(user.id))
            os.mkdir(folder_path)

            #profile = UserProfile(user = user, slug = user.username)
            profile = profile_form.save(commit = False)
            profile.user = user
            profile.slug = user.username

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()


            registered = True

        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'fooodie/register.html', context = {'user_form' : user_form,
                                                               'profile_form' : profile_form,
                                                               'registered' : registered})

def user_logout(request):
    context_dict = {}

    response = render(request, 'fooodie/home.html')
    return response

# May need to use multiple views for profiles; will try
# to figure out if view can used for both myprofile
# and other user profiles
def user_profile(request):
    context_dict = {}

    response = render(request, 'fooodie/home.html')
    return response

def add_food_photo(request):
    context_dict={}
    response=render(request, 'fooodie/uploadfoodphoto.html')

@login_required
def myprofile(request): #User's manage account site
    context_dict = {}
    response = render(request, 'fooodie/myprofile.html')
    return response
# Create your views here.
