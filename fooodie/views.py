from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from fooodie.models import Photo, UserProfile
from fooodie.forms import UserForm, UserProfileForm, PhotoForm, ChangeUsername, ChangeEmail, ChangePicture
from datetime import datetime
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
import os, random, string
from django.views import View

#####################################HELPER FUNCTIONS START
def profile_leaderboard(profile):
    top_profiles_set = UserProfile.objects.order_by('-totalVotes')
    top_profiles = []
    position_leaderboard = 0
    profile_votes=['-1']
    for userprofile in top_profiles_set: #Creates new List containing tuples (UserProfile,Position)
        if profile_votes[len(profile_votes)-1]!=userprofile.totalVotes:
            position_leaderboard +=  1
        profile_votes.append(userprofile.totalVotes)
        if profile==userprofile:
            break
    return position_leaderboard

#Returns two randomly-chosen Photo objects from the database
def random_dif_pics():
    pics = Photo.objects.order_by('?')
    pics_to_choose = pics[:2]
    pic1= pics_to_choose.first()
    pic2=pics_to_choose[1]
    if pic1==pic2:
        return random_dif_pics()
    return pic1, pic2

####################################HELPER FUNCTIONS END

###########VIEWS
def home(request):
    context_dict = {}
    pics = Photo.objects.order_by('?')
    try:
        photo1, photo2=random_dif_pics() #Returns two randomly-selected Photo objects into photo1 and photo2
        context_dict['photo1']=photo1
        context_dict['photo2']=photo2
        visitor_cookie_handler(request) #Tracks visit count and last visit time via a server-side cookie
        random_pics = pics[:3]
        context_dict['random_pics'] = random_pics
        context_dict['visits'] = request.session['visits'] #Obtains number of visits made this session
    except:
        return render(request, 'fooodie/error.html', context={'error' : "DEV NOTE: If this happens, it means there has been an issue when populating the database... Maybe you forgot to migrate or you didn't run the populate script. As long as you don't click on anything it is fine though. First stop running the server. Then go to your files and delete both [workspace]/fooodie/db.sqlite3, and [workspace]/fooodie/media with all its contents. Then in command line go to [workspace]/fooodie/ and first run 'python manage.py migrate', second run 'python populate_fooodie.py'. PLEASE DO NOT CLICK ON ANYTHING ON THE PAGE UNTIL YOU DO THIS. YOU'LL ONLY BREAK IT EVEN MORE"})
    return render(request, 'fooodie/home.html', context = context_dict)

def about(request):
    context_dict = {}
    response = render(request, 'fooodie/about.html')
    return(response)

def leaderboard(request):
    context_dict = {}
    top_pics = Photo.objects.order_by('-votes')[:3] #Top 3
    context_dict['top_pics'] = top_pics

    top_profiles_set = UserProfile.objects.order_by('-totalVotes')[:10] #Top 0 - 10
    top_profiles = []
    position_leaderboard = 0
    profile_votes=['-1']
    for profile in top_profiles_set: #Creates new List containing tuples (UserProfile,Position)
        if profile_votes[len(profile_votes)-1]!=profile.totalVotes:
            position_leaderboard +=  1
        top_profiles.append((profile,position_leaderboard))
        profile_votes.append(profile.totalVotes)

    context_dict['top_profiles'] = top_profiles

    response = render(request, 'fooodie/leaderboard.html', context = context_dict)
    return(response)

#REGISTRATION/LOG IN/LOG OUT STARTS
#This will simply display the forms; the associated template will call
#one of the functions below dependent on button clicked
def loginregister(request):
    if request.user.is_authenticated:
        return render(request, 'fooodie/error.html', context={'error':"You're already logged in. If you want to log in as someone else, please log out first."})
    registered = False
    user_form = UserForm()
    user_form.fields['username'].widget.attrs['maxlength']='20'
    profile_form = UserProfileForm()

    return render(request, 'fooodie/loginregister.html', context = {'user_form' : user_form,
                                                               'profile_form' : profile_form,
                                                               'registered' : registered})

def userlogin(request):
    if request.user.is_authenticated:
        return redirect(reverse('fooodie:loginregister'))
    user_form=UserForm()
    user_form.fields['username'].widget.attrs['maxlength']='20'
    profile_form=UserProfileForm()
    if request.method == 'POST': #If input data is being sent to the server
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username = username, password = password) #Verifies credentials against user database, returns appropriate User object if valid
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('fooodie:myprofile'))
            else:
                return render(request, 'fooodie/loginregister.html', context = {'user_form' : user_form, 'profile_form' : profile_form , 'login_error' : "Your account has been disabled. We'd apologize... But you probably did something to earn this.",})
        else:
            return render(request, 'fooodie/loginregister.html', context = {'user_form' : user_form, 'profile_form' : profile_form, 'login_error':"Invalid login details supplied."})
    else:
        return redirect(reverse('fooodie:loginregister'))

#Will focus on the registration/login logic first, implement into a single view later
def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('fooodie:loginregister')) #Redirects back to login/register page if already logged in
    context_dict={}
    if request.method == 'POST': #If input data is being sent to the server
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid(): #Two forms make up the entire registration form and so must both be valid
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user
            profile.slug = user.username
            profile.save() #Profile must be saved in order to generate an id value to be used next

            if 'picture' in request.FILES:
                picture=request.FILES['picture'] #Obtains profile picture from request
                picture.name=str(profile.id)+".jpg"
                profile.picture=picture #UserProfile model handles save location of profile picture upon save
                profile.save()

            user.backend='django.contrib.auth.backends.ModelBackend'
            #Specify backend used for log in as we have 2 log in backends (Social and standard Django)
            login(request, user)
            return redirect(reverse('fooodie:myprofile'))

        else:
            context_dict['register_error']=user_form.errors
            user_form = UserForm()
            user_form.fields['username'].widget.attrs['maxlength']='20'
            context_dict['user_form'] = user_form
            context_dict['profile_form']=UserProfileForm()                
            return render(request, 'fooodie/loginregister.html', context = context_dict)
    else:
        return(redirect(reverse('fooodie:loginregister')))

@login_required
def userlogout(request):
    logout(request) # Since we know the user is logged in, we can now just log them out.
    return redirect(reverse('fooodie:home'))
#REGISTRATION/LOG IN/LOG OUT ENDS

#ADD AND DELETE PICTURE FUNCTIONALITY STARTS
@login_required
def addfoodphoto(request):
    profile=UserProfile.objects.get(user=request.user)
    context_dict = {}
    context_dict['profile'] = profile
    context_dict['photo_type']="food photo"
    context_dict['food']=True
    if request.method == 'POST':
        photo_form = PhotoForm(request.POST) # If the form is valid...
        if photo_form.is_valid(): # Save the photo form data to the database.
            # Now sort out the UserProfile instance. # Since we need to set the user attribute ourselves, we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            try:
                photo = photo_form.save(commit=False)
                photo.user = profile # Did the user provide a profile picture? If so, we need to get it from the input form and put it in the UserProfile model.
                photo.photo = request.FILES['photo']
                # Now we save the UserProfile model instance.
                photo.save() # Update our variable to indicate that the template registration was successful.
                return redirect(reverse('fooodie:myprofile'))
            except:
                context_dict['error']="There was something wrong with your upload. Please try again. When this happens it's usually because you didn't upload a picture"
        else: # Invalid form or forms - mistakes or something else? Print problems to the terminal.
            context_dict['error']=photo_form.errors
    else: # Not a HTTP POST, so we render our form using two ModelForm instances. # These forms will be blank, ready for user input.
        photo_form = PhotoForm()
        photo_form.fields['name'].widget.attrs['maxlength']='20'
    context_dict['form'] = photo_form
    return render(request, 'fooodie/addpropic.html', context = context_dict)

@login_required
def deletepic(request, photo_id):
    photo = Photo.objects.get(id = photo_id)

    #Author's totalVotes must be decreased to reflect deletion of photo and thus non-contribution of the photo's votes
    author = UserProfile.objects.get(id = photo.user.id)
    author.totalVotes = author.totalVotes - photo.votes
    author.save()
    
    photo.delete()
    return redirect(reverse('fooodie:myprofile'))
#ADD AND DELETE PICTURE FUNCTIONALITY ENDS

#MYPROFILE AND MYPROFILE SETTINGS START
@login_required
def myprofile(request): #User's manage account site
    user = request.user
    context_dict={}
    context_dict['user'] = user
    context_dict['my_profile']=True
    try:
        profile = UserProfile.objects.get(user = user)
        context_dict['profile'] = profile
        photos = Photo.objects.filter(user = profile) #Get all the pictures with user_id. Useful documentation of this notation (user__id with two underscores)
        context_dict['photos'] = photos
        context_dict['position'] = profile_leaderboard(profile)

        #NUMBER OF PICS COUNTER
        i = 0
        for picture in photos:
            i = i + 1
        context_dict['totalPhotos'] = i #Variable Used in Counter
        #NUMBER OF PICS COUNTER ENDS
    except:
        pass #IF THIS HAPPENS IT MEANS YOU'RE USING AN USER THAT DOESN'T HAVE A PROFILE, MOST LIKELY A SUPERUSER.
    return render(request, 'fooodie/profile.html', context = context_dict)

@login_required
def usersettings(request):
    context_dict = {}
    user = request.user
    profile = UserProfile.objects.get(user = user)
    context_dict['profile'] = profile
    photos = Photo.objects.filter(user__id = profile.id) #Get all the pictures with user_id. Useful documentation of this notation (user__id with two underscores)
    context_dict['photos'] = photos
    response = render(request, 'fooodie/settings.html', context = context_dict)
    return response

@login_required
def settingsusername(request):
    user = request.user
    profile=UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        name_form = ChangeUsername(request.POST) # If the form is valid...
        if name_form.is_valid():
            user.username = name_form.cleaned_data['username'] #As ChangeUsername is a basic form, form fields must be matched to model fields
            user.save()
            return redirect(reverse("fooodie:settings"))
        else: # Invalid form or forms - mistakes or something else? Print problems to the terminal.
            print(name_form.errors)
    else: # Not a HTTP POST, so we render our form using two ModelForm instances. # These forms will be blank, ready for user input.
        name_form = ChangeUsername()
    return render(request, 'fooodie/changesettings.html', context={'change': 'username', 'form':name_form, 'profile':profile, 'originalvalue':profile.user.username})

@login_required
def settingsemail(request):
    user = request.user
    profile=UserProfile.objects.get(user=request.user)
    if profile.google:
        return render(request, 'fooodie/error.html', context={'error' : 'An account made with google cannot change its email!'})
    if request.method == 'POST':
        email_form = ChangeEmail(request.POST) # If the form is valid...
        if email_form.is_valid():
            user.email = email_form.cleaned_data['email']
            user.save()
            return redirect(reverse("fooodie:settings"))
        else: # Invalid form or forms - mistakes or something else? Print problems to the terminal.
            print(email_form.errors)
    else: # Not a HTTP POST, so we render our form using two ModelForm instances. # These forms will be blank, ready for user input.
        email_form = ChangeEmail()
    return render(request, 'fooodie/changesettings.html', context={'change': 'email', 'form':email_form, 'profile':profile, 'originalvalue':profile.user.email})

@login_required
def settingsprofilepic(request):
    profile = UserProfile.objects.get(user = request.user) #Obtains current logged-in user that sent the request
    context_dict = {}
    if request.method == 'POST': #Request type must be POST, as input data must be provided
        profile_pic_form = ChangePicture(request.POST)
        if profile_pic_form.is_valid():
            try:
                picture=request.FILES['picture'] #Obtaining picture from request
                picture.name=str(profile.id)+".jpg" #Using same naming scheme as that which registration uses
                profile.picture=picture
                profile.save()
                return redirect(reverse('fooodie:myprofile'))
            except:
                context_dict['error']="There was something wrong with your upload. Please try again. When this happens it's usually because you didn't upload a picture"
        else:
            profile_pic_form = ChangePicture()
            context_dict['error']=profile_pic_form.errors #Flags errors on form fields, informing viewer of issues with input

    else:
        profile_pic_form = ChangePicture()
    context_dict['form'] = profile_pic_form
    context_dict['profile'] = profile
    context_dict['photo_type']="profile picture"

    return render(request, 'fooodie/addpropic.html', context = context_dict )

@login_required
def deleteaccount(request):
    user=request.user
    logout(request)
    user.delete() #Utilising inbuilt delete() function to remove User object from database
    return redirect(reverse('fooodie:home'))


@login_required
def settingspassword(request):
    user = request.user
    profile=UserProfile.objects.get(user=request.user)
    if profile.google: #Boolean field that is true if profile was created via Google authentication
        return render(request, 'fooodie/error.html', context={'error' : 'An account made with google works without a password, so you cannot change it!'})
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect( reverse("fooodie:settings"))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'fooodie/changesettings.html', {
        'change': 'password', 'form':form, 'profile':profile, 'originalvalue':"Just kidding, displaying your password would be so unsafe!"
    })
#MYPROFILE SETTINGS END

#COOKIE STUFF STARTS
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
#COOKIE STUFF ENDS

#SEARCH AND USER PROFILE STARTS
def usersearch(request):
    username=request.GET.get('search')
    try:
        profile=UserProfile.objects.get(user__username=username)
    except:
        return render(request, 'fooodie/error.html', context={'error' :"We're sorry but the user "+str(username)+" does not exist. Please try again. Remember you have to write the user's exact name. Uppercase and lowercase matters! (You can check names in the leaderboard)"})
    return redirect(reverse('fooodie:userprofile', args=[profile.slug]))

def userprofile(request, user_profile_slug):
    try:
        profile = UserProfile.objects.get(slug = user_profile_slug)
        context_dict = {}
        context_dict['profile'] = profile
        photos = Photo.objects.filter(user = profile) #Get all the pictures with user_id. Useful documentation of this notation (user__id with two underscores)
        context_dict['photos'] = photos
        context_dict['position'] = profile_leaderboard(profile) #Function declared at bottom of page

        #NUMBER OF PICTURE COUNTER STARTS
        i = 0
        for picture in photos:
            i = i + 1
        context_dict['totalPhotos'] = i
        #NUMBER OF PICTURE COUNTER ENDS
    except:
        return render(request, 'fooodie/profile.html', context = {'user_searched' : user_profile_slug})
    return render(request, 'fooodie/profile.html', context = context_dict)
#SEARCH AND USER PROFILE ENDS

#GOOGLE ACCOUNT LOG IN STARTS
def googleloggedin(request):
    user=request.user
    try:
        profile = UserProfile.objects.get(user=user)
    except:
        profile = UserProfile(user=user)
        profile.google=True
        profile.save()
    return redirect(reverse('fooodie:myprofile'))
# GOOGLE ACCOUNT LOG IN ENDS

#Receives AJAX request from code executed when a "like" button is clicked
class LikePhoto(View):
    def get(self, request):
        photo_id = request.GET['photo_id'] #Obtains photo id from AJAX request
        try:
            photo = Photo.objects.get(id = int(photo_id)) #Retrieves Photo object with id matching passed id; id is the object's primary key
        except Photo.DoesNotExist:
            return redirect(reverse('fooodie:home'))
        except ValueError:
            return redirect(reverse('fooodie:home'))

        #Increments the the vote tallies of the picture and the picture's associated user
        author = UserProfile.objects.get(id = photo.user.id)
        photo.votes = photo.votes + 1
        author.totalVotes = author.totalVotes + 1;
        photo.save()
        author.save()

        photo1, photo2=random_dif_pics()

        #Construct JSON-formatted response data. AJAX handles a plain text (HTML), JSON or
        #XML-formatted response; as multiple pieces of text data must be returned, JSON is most
        #suitable for the task, with the added benefit of utilising standard JavaScript functions
        #to parse the JSON data returned
        return_dict = {'photo1' :
                       {'url' : photo1.photo.url,
                        'name' : photo1.name,
                        'username' : photo1.user.user.username,
                        'votes' : photo1.votes,
                        'id' : photo1.id},
                       'photo2' :
                       {'url' : photo2.photo.url,
                        'name' : photo2.name,
                        'username' : photo2.user.user.username,
                        'votes' : photo2.votes,
                        'id' : photo2.id}
                       }

        #Return the JSON-formatted data above
        return JsonResponse(return_dict)

# Create your views here.
