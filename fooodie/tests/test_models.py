from django.test import TestCase
from fooodie.models import UserProfile, Photo, UserFactory
import factory
import factory.django

class UserProfileTestCase(TestCase):
    def test_createWorks(self):
        user1=UserFactory()
        user1.set_password("FooodieIsAwesome")
        user1.save()
        UserProfile.objects.create(user=user1, totalVotes=10)

class PhotoTestCase(TestCase):
    def test_createWorks(self):
        user1=UserFactory()
        user1.set_password("FooodieIsAwesome")
        user1.save()
        profile=UserProfile.objects.create(user=user1, totalVotes=10)
        
        Photo.objects.create(name="Pizza", photo="", user=profile)