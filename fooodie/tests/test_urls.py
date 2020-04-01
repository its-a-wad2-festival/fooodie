from django.test import TestCase
from django.urls import reverse, resolve
from fooodie.views import *
from fooodie.models import UserProfile, Photo, UserFactory
import factory
import factory.django

# 'fooodie:likephoto':likephoto, 'fooodie:loginregister':loginregister,

class TestUrls(TestCase):   
    def CreateUserProfile(self): #Create UserProfile so we can test it
        user1=UserFactory()
        user1.set_password("JoseIsAwesome")
        user1.save()
        profile=UserProfile.objects.create(user=user1, totalVotes=10)
        return profile
        
    def test_home_url_is_resolved(self):
        url=reverse('fooodie:home')
        self.assertEquals(resolve(url).func, home)
        
    def test_loginregister_url_is_resolved(self):
        url=reverse('fooodie:loginregister')
        self.assertEquals(resolve(url).func, loginregister)
        
    def test_about_url_is_resolved(self):
        url=reverse('fooodie:about')
        self.assertEquals(resolve(url).func, about)
        
    def test_leaderboard_url_is_resolved(self):
        url=reverse('fooodie:leaderboard')
        self.assertEquals(resolve(url).func, leaderboard)
        
    def test_myprofile_url_is_resolved(self):
        url=reverse('fooodie:myprofile')
        self.assertEquals(resolve(url).func, myprofile)

    def test_settings_url_is_resolved(self):
        url=reverse('fooodie:settings')
        self.assertEquals(resolve(url).func, usersettings)
    
    def test_deletepic_url_is_resolved(self):
        url=reverse('fooodie:deletepic', args={'photo_id': int(5)})#Random testing number
        self.assertEquals(resolve(url).func, deletepic)
    
    def test_settingspassword_url_is_resolved(self):
        url=reverse('fooodie:settingspassword')
        self.assertEquals(resolve(url).func, settingspassword)
    
    def test_register_url_is_resolved(self):
        url=reverse('fooodie:register')
        self.assertEquals(resolve(url).func, register)
    
    def test_settingsusername_url_is_resolved(self):
        url=reverse('fooodie:settingsusername')
        self.assertEquals(resolve(url).func, settingsusername)
    
    def test_settingsprofilepic_url_is_resolved(self):
        url=reverse('fooodie:settingsprofilepic')
        self.assertEquals(resolve(url).func, settingsprofilepic)
    
    def test_settingsemail_url_is_resolved(self):
        url=reverse('fooodie:settingsemail')
        self.assertEquals(resolve(url).func, settingsemail)
        
    def test_usersearch_url_is_resolved(self):
        url=reverse('fooodie:usersearch')
        self.assertEquals(resolve(url).func, usersearch)
    
    def test_userprofile_url_is_resolved(self):
        url=reverse('fooodie:userprofile', args={'user_profile_slug': "randomstringfortesting"})
        self.assertEquals(resolve(url).func, userprofile)
        
    def test_logout_url_is_resolved(self):
        url=reverse('fooodie:logout')
        self.assertEquals(resolve(url).func, userlogout)
        
    def test_login_url_is_resolved(self):
        url=reverse('fooodie:login')
        self.assertEquals(resolve(url).func, userlogin)
        
    def test_googleloggedin_url_is_resolved(self):
        url=reverse('fooodie:googleloggedin')
        self.assertEquals(resolve(url).func, googleloggedin)
        
    def test_addfoodphoto_url_is_resolved(self):
        url=reverse('fooodie:addfoodphoto')
        self.assertEquals(resolve(url).func, addfoodphoto)
    
    def TestUrlIsResolved(self, name):
        url=reverse(name)
        self.assertEquals(resolve(url).func, urls_views[name])