from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
        
class UserProfile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) #Links UserProfile to a User model instance.  
    slug=models.SlugField(unique=True) #Slug field for when we try to view other user's profiles (Part of the urls)
    picture=models.ImageField(upload_to="profilepics", blank=True)
    totalVotes = models.IntegerField(default=0)
    # We store within a user the number of votes he has, each time someone votes on a photo we update both Photo.votes and UserProfile.totalVotes.
    # This way we only have to iterate through the list of UserProfile in the leaderboard.
    # When accessing a user's profile you just order the leaderboard using the totalVotes attribute and then iterate through it to find him.
    # Once you do his position on the list is his position in the ranking
    
    #IDEA 1 would require more functions in the views, and is a timely operation, yet should be memory efficient as we're storing less data
    #IDEA 2 is less memory efficient but saves us lots of time with calculations.
    #Personally I feel IDEA 2 is better.

class Photo(models.Model):
    NAME_MAX_LENGTH=128
    name = models.CharField(max_length=NAME_MAX_LENGTH) #The name the user wants to give to the picture he has uploaded
    votes=models.IntegerField(default=0) #Number of votes the picture has
    photo = models.ImageField(upload_to="photos") #Uploaded photo (Django handles all of this, so we don't ahve to worry about paths)
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE) #User which uploaded the photo, 1 to MANY relation, so primary key on MANY side
