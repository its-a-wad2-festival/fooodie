import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'wad2_group_project.settings')

import django
django.setup()
from django.contrib.auth.models import User
from fooodie.models import Photo, UserProfile, UserFactory
import random
import os
import factory  
import factory.django

#Variable declaration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(os.path.join(BASE_DIR, 'media'))


#Might be useful to create random data for users: stackoverflow.com/questions/33024510/populate-django-database

def create_user_profile():
    user = UserFactory()
    print(user.first_name,user.last_name,user.username,user.email)
    user.set_password("JoseIsAwesome")
    user.save()
    profile = UserProfile(user=user, slug = user.username)
    profile.save()
    folder_path = os.path.join(MEDIA_DIR, user.username)
    os.mkdir(folder_path)
     
if __name__ == '__main__':
    print('Starting fooodie population script...')
    for i in range (0,20):
        create_user_profile()
