import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'wad2_group_project.settings')

import django
django.setup()
from django.contrib.auth.models import User
from fooodie.models import Photo, UserProfile
import random
import os

#Variable declaration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(os.path.join(BASE_DIR, 'media'))


#Might be useful to create random data for users: stackoverflow.com/questions/33024510/populate-django-database

def create_user_profile():
    user = User.objects.create_user("a","a@gmail.com","12gol34demessi")
    profile = UserProfile(user=user)
    profile.save()
    folder_path = os.path.join(MEDIA_DIR, user.username)
    os.mkdir(folder_path)
     
if __name__ == '__main__':
    print('Starting fooodie population script...')
    create_user_profile()
