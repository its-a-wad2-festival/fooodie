from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from fooodie.models import Photo, UserProfile
from fooodie.forms import UserForm, UserProfileForm, PhotoForm
from datetime import datetime
import os, random


def home(request):
    context_dict = {}
    context_dict['userProfiles']=UserProfile.objects.all()
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

    photo1=pics_to_choose.first()
    context_dict['photo1']=photo1

    photo2=pics_to_choose[1]
    context_dict['photo2']=photo2

    context_dict['pics_to_choose'] = pics_to_choose

    random_pics = pics[:3]
    context_dict['random_pics'] = random_pics

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'fooodie/home.html', context = context_dict)
    return(response)

def about(request):
    context_dict = {}
    context_dict['userProfiles']
    response = render(request, 'fooodie/about.html')
    return(response)

def leaderboard(request):
    context_dict = {}
    context_dict['userProfiles']=UserProfile.objects.all()
    top_pics = Photo.objects.order_by('-votes')[:3] #Top 3
    context_dict['top_pics'] = top_pics

    top_profiles = UserProfile.objects.order_by('-totalVotes')[:8] #Top 8
    context_dict['top_profiles'] = top_profiles

    response = render(request, 'fooodie/leaderboard.html', context = context_dict)
    return(response)

#This will simply display the forms; the associated template will call
#one of the functions below dependent on button clicked
def user_signup_login(request):
    registered = False
    user_form = UserForm()
    profile_form = UserProfileForm()

    return render(request, 'fooodie/loginregister.html', context = {'user_form' : user_form,
                                                               'profile_form' : profile_form,
                                                               'registered' : registered})
##    context_dict = {}
##    context_dict['userProfiles']=UserProfile.objects.all()
##
##    response = render(request, 'fooodie/home.html')
##    return response

#Will focus on the registration/login logic first, implement into a single view later
def user_login(request):
    if request.method == 'POST':
        #Need to consider allowing email OR username potentially
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                login(request, user)
                print("Login success!")
                print("Is user thenticated?")
                print(user.is_authenticated)
                return redirect(reverse('fooodie:home'))
            else:
                return HttpResponse("Your account is disabled")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, 'fooodie/loginregister.html')

#Will focus on the registration/login logic first, implement into a single view later
def register(request):
    registered=True
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            #print('user id: '+str(user.id))

            #Creating the user's folder so we can put the profile pic into it
##            folder_path = os.path.join(settings.MEDIA_DIR, str(user.id))
##            os.mkdir(folder_path)
##
##            print('folder path: '+folder_path)
##
##            folder_path_str = str(folder_path)

            ##Think about placing the photo in the directory THEN just linking to that
            ##photo, like profile.picture = path_to_file

##            if 'picture' in request.FILES:
##                pro_pic = request.FILES['picture']
##                pro_pic2 = Image.open(pro_pic)
##                pro_pic2.filename = str(user.id)+'.jpg'
##                print('filename: '+pro_pic2.filename)
##                #filename = pro_pic.filename
##                pro_pic2.save(folder_path)

            #profile = UserProfile(user = user, slug = user.username)
##            profile_pic = request.FILES['picture']
##            path = default_storage.save(folder_path+'\\image.jpeg', ContentFile(profile_pic.read()))
            profile = profile_form.save(commit = False)
            profile.user = user
            profile.slug = user.username
            #profile.picture = path

            profile.save()

            profile_pic_path = os.path.join(settings.MEDIA_DIR, str(profile.id))
            os.mkdir(profile_pic_path)

            if 'picture' in request.FILES:
                profile_pic = request.FILES['picture']
                extension = profile_pic.name.split('.')[-1] #Gets the string after the last period, to deal with name.txt.jpg situations
                path_to_pic = default_storage.save(profile_pic_path+'\\'+str(profile.id)+'_propic.'+extension, ContentFile(profile_pic.read()))
                profile.picture = path_to_pic
                profile.save()

            print('So USER id is '+str(user.id)+' and PROFILE id is '+str(profile.id)+' and picture is '+str(profile.picture))


            registered = True

        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'fooodie/loginregister.html', context = {'user_form' : user_form,
                                                               'profile_form' : profile_form,
                                                               'registered' : registered})

@login_required
def user_logout(request):
    logout(request) # Since we know the user is logged in, we can now just log them out.

@login_required
def user_logout(request):
    logout(request) # Since we know the user is logged in, we can now just log them out.
    return redirect(reverse('fooodie:home'))


def user_profile(request, user_profile_slug):
    context_dict = {}
    context_dict['userProfiles']=UserProfile.objects.all()
    user = request.user
    context_dict = {}
    try:
        profile = UserProfile.objects.get(slug = user_profile_slug)
        context_dict['profile'] = profile
        photos = Photo.objects.filter(user = profile) #Get all the pictures with user_id. Useful documentation of this notation (user__id with two underscores)
        context_dict['photos'] = photos
    except:
        pass
    return render(request, 'fooodie/userprofile.html', context = context_dict)

def add_food_photo(request):
    context_dict = {}
    context_dict['userProfiles']=UserProfile.objects.all()
    response=render(request, 'fooodie/uploadfoodphoto.html')

@login_required
def myprofile(request): #User's manage account site
    context_dict = {}
    context_dict['userProfiles']=UserProfile.objects.all()
    user = request.user

    #profile.user.username=''

    try:
        profile = UserProfile.objects.get(user = user)
        context_dict['profile'] = profile
        photos = Photo.objects.filter(user__id = profile.id) #Get all the pictures with user_id. Useful documentation of this notation (user__id with two underscores)
        context_dict['photos'] = photos
    except:
        pass
    context_dict['user'] = user

    if 'search' in request.GET:
        profile.user.username = request.GET['search']
        #fooodie = fooodie.filter(text__icontains=search_terms)

    context = {'profile.user.username' : profile.user.username}

    response = render(request, 'fooodie/myprofile.html', context = context_dict)
    return response


def addfoodphoto(request):
    added = False # If it's a HTTP POST, we're interested in processing form data.
    profile=UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        photo_form = PhotoForm(request.POST) # If the form is valid... 
        if photo_form.is_valid(): # Save the photo form data to the database. 
            # Now sort out the UserProfile instance. # Since we need to set the user attribute ourselves, we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems. 
            photo = photo_form.save(commit=False) 
            photo.user = user # Did the user provide a profile picture? If so, we need to get it from the input form and put it in the UserProfile model. 
            photo.photo = request.FILES['photo'] 
            # Now we save the UserProfile model instance. 
            photo.save() # Update our variable to indicate that the template registration was successful. 
            added = True 
        else: # Invalid form or forms - mistakes or something else? Print problems to the terminal. 
            print(photo_form.errors) 
    else: # Not a HTTP POST, so we render our form using two ModelForm instances. # These forms will be blank, ready for user input. 
        photo_form = PhotoForm()  
    return render(request, 'fooodie/addPic.html', context = {'photo_form' : photo_form,
                                                               'registered' : added})

####SETTINGS VIEWS
@login_required
def settings(request):
    context_dict = {}
    context_dict['userProfiles']=UserProfile.objects.all()
    user = request.user
    profile = UserProfile.objects.get(user = user)
    context_dict['profile'] = profile
    photos = Photo.objects.filter(user__id = profile.id) #Get all the pictures with user_id. Useful documentation of this notation (user__id with two underscores)
    context_dict['photos'] = photos
    response = render(request, 'fooodie/settings.html', context = context_dict)
    return response

@login_required
def deletepic(request, photo_id):
    Photo.objects.filter(id = photo_id).delete()
    return redirect(reverse('fooodie:settings'))

@login_required
def settingsusername(request):
    context_dict = {}
    context_dict['userProfiles']=UserProfile.objects.all()
    user = request.user
    #Get new username from forms!
    user.username=newusername
    user.save()
    return redirect(reverse('fooodie:settings'))

@login_required
def settingsemail(request):
    context_dict = {}
    context_dict['userProfiles']=UserProfile.objects.all()
    user = request.user
    #Get new email from forms!
    user.email=newemail
    user.save()
    return redirect(reverse('fooodie:settings'))

@login_required
def settingsprofilepic(request):
    context_dict = {}
    context_dict['userProfiles']=UserProfile.objects.all()
    user = request.user
    profile=UserProfile.objects.get(user=user)
    #Get Profilepic from forms
    profile.profilepic=newprofilepic
    profile.save()
    context_dict['change']
    return redirect(reverse('fooodie:settings'))

@login_required
def settingspassword(request):
    pass
##SETTINGS END

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request,'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1

        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits



# Create your views here.
