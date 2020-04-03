from django.test import TestCase
from fooodie.models import User, UserProfile, Photo, UserFactory
import factory
import factory.django

class TestCreateModels(TestCase):
    def setUp(self):
        user1=UserFactory()
        user1.username="Test"
        user1.set_password("FooodieIsAwesome")
        user1.save()

    def test_profile_create_works(self):
        user1=User.objects.get(username="Test")
        UserProfile.objects.create(user=user1, totalVotes=10)
    
    def test_create_photo_works(self):
        user1=User.objects.get(username="Test")
        profile=UserProfile.objects.create(user=user1, totalVotes=10)        
        Photo.objects.create(name="Pizza", photo="", user=profile)

class TestAttributes(TestCase):
    def setUp(self):
        user1=UserFactory()
        user1.username="Test"
        user1.set_password("FooodieIsAwesome")
        user1.save()
        profile=UserProfile.objects.create(user=user1, totalVotes=0)
        Photo.objects.create(name="Pizza", photo="", user=profile)

    def test_profile_username(self):
        user=User.objects.get(username="Test")
        profile=UserProfile.objects.get(user=user)
        self.assertEquals(profile.user.username, user.username)
    
    def test_profile_email(self):
        user=User.objects.get(username="Test")
        profile=UserProfile.objects.get(user=user)
        self.assertEquals(profile.user.email, user.email)
        
    def test_profile_password(self):
        user=User.objects.get(username="Test")
        profile=UserProfile.objects.get(user=user)
        self.assertEquals(profile.user.password, user.password)
    
    def test_photo_votes(self):
        pic=Photo.objects.get(name="Pizza")
        pic.increase_votes(5)
        self.assertEquals(pic.votes, 5)
        
    def test_profile_votes(self):
        pic=Photo.objects.get(name="Pizza")
        pic.increase_votes(5)
        profile=pic.user
        self.assertEquals(profile.totalVotes, 5)
        
    def test_multiple_photo_votes(self):
        user=UserFactory()
        profile=UserProfile.objects.create(user=user, totalVotes=0)
        apple=Photo.objects.create(name="Apple", photo="", user=profile)
        banana=Photo.objects.create(name="Banana", photo="", user=profile)
        apple.increase_votes(9)
        banana.increase_votes(4)
        apple.decrease_votes(7)
        self.assertEquals(profile.totalVotes, 6)