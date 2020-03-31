from django.test import TestCase, Client
from fooodie.models import UserProfile, Photo, UserFactory

class UserFactoryTestCase(factory.django.DjangoModelFactory):
    def createWorks(self):
		user1=UserFactory.objects.create()
        user1.set_password("JoseIsAwesome")
        user1.save()
	
class UserProfileTestCase(TestCase):
	def createWorks(self):
        user1=UserFactory.objects.create()
        user1.set_password("JoseIsAwesome")
        user1.save()
        
		UserProfile.objects.create(user=user1, totalVotes=10)

class PhotoTestCase(TestCase):
	def createWorks(self):
        user1=UserFactory.objects.create()
        user1.set_password("JoseIsAwesome")
        user1.save()
        
		profile=UserProfile.objects.create(user=user1, totalVotes=10)
		Photo.objects.create(name="Pizza", photo="", user=profile)
