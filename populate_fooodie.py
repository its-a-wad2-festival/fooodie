import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'wad2_group_project.settings')

import django
django.setup()
import factory  
import factory.django
import django.contrib.auth
from foodie.models import Photo, UserProfile
import random

#Might be useful to create random data for users: stackoverflow.com/questions/33024510/populate-django-database


