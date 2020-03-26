from django.db import models
from time import time
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import factory  
import factory.django
        
class UserProfile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE) #Links UserProfile to a User model instance.  
    slug=models.SlugField(unique=True) #Slug field for when we try to view other user's profiles (Part of the urls)
    picture=models.ImageField(blank=True)
    #picture=models.ImageField(upload_to=str(id), blank=True)
    totalVotes = models.IntegerField(default=0)
    
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)
        
    #We need to add __str__ method here

    # We store within a user the number of votes he has, each time someone votes on a photo we update both Photo.votes and UserProfile.totalVotes.
    # This way we only have to iterate through the list of UserProfile in the leaderboard.
    # When accessing a user's profile you just order the leaderboard using the totalVotes attribute and then iterate through it to find him.
    # Once you do his position on the list is his position in the ranking

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        #Here we tell the UserFactory to use the model User as a base,
        #this means it creates a User object and edits its following parameters:
    username = factory.Faker('user_name') #Changes "username" parameter of the user created above to a random "username", generated by the Faker function
    email = factory.Faker('email') #Changes "email" parameter of the user created above to a random "email", generated by the Faker function


""" 
These two functions are necessary to change the default folder
where photos are stored when uploaded by an user
"""

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/userProfile<id>
    return '{0}'.format(instance.userProfile.id)

def get_upload_filename(userpic,name):
    return u'%s/%s_%s' % (str(userpic.user.id),
                          str(time()).replace('.', '_'),
                          name)
        
class Photo(models.Model):
 
    NAME_MAX_LENGTH=128
    name = models.CharField(max_length=NAME_MAX_LENGTH) #The name the user wants to give to the picture he has uploaded
    votes=models.IntegerField(default=0) #Number of votes the picture has
    user= models.ForeignKey(UserProfile, on_delete=models.CASCADE) #User which uploaded the photo, 1 to MANY relation, so primary key on MANY side
    photo = models.ImageField(blank=True, upload_to = get_upload_filename) #Uploaded photo
    
    def __str__(self):
        return self.name
        
