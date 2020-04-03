from django.test import TestCase, Client
from fooodie.models import UserProfile, Photo, UserFactory
from fooodie.views import *

#We make sure that all views return something when you're not logged in, as so the program doesn't render any error pages.
#We ensure that all accounts with a login required tag are redirected to the registerlogin view
class ViewsTestCaseWithoutLogIn(TestCase):
    def setup(self):
        self.client=Client()

    def test_home_view_status_200(self):
        response=self.client.get(reverse('fooodie:home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fooodie/error.html')
        
    def test_deleteaccount_view_status_200(self):
        response=self.client.get(reverse('fooodie:deleteaccount'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fooodie/loginregister.html')
    
    def test_about_view_status_200(self):
        response=self.client.get(reverse('fooodie:about'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fooodie/about.html')
        
    def test_leaderboard_view_status_200(self):
        response=self.client.get(reverse('fooodie:leaderboard'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fooodie/leaderboard.html')

    def test_loginregister_view_status_200(self):
        response=self.client.get(reverse('fooodie:loginregister'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fooodie/loginregister.html')

    def test_userlogin_view_status_200(self):
        response=self.client.get(reverse('fooodie:login'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fooodie/loginregister.html')

    def test_register_view_status_200(self):
        response=self.client.get(reverse('fooodie:register'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fooodie/loginregister.html')
        
    def test_userlogout_view_status_200(self):
        response=self.client.get(reverse('fooodie:logout'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fooodie/loginregister.html')

    def test_addfoodphoto_view_status_200(self):
        response=self.client.get(reverse('fooodie:addfoodphoto'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fooodie/loginregister.html')

    def test_deletepic_view_status_200(self):
        response=self.client.get(reverse('fooodie:deletepic', args={'user_profile_slug': 7}), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fooodie/loginregister.html')

    def test_myprofile_view_status_200(self):
        response=self.client.get(reverse('fooodie:myprofile'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fooodie/loginregister.html')
        
    def test_settingsemail_view_status_200(self):
        response=self.client.get(reverse('fooodie:settingsemail'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fooodie/loginregister.html')

    def test_settingsprofilepic_view_status_200(self):
        response=self.client.post(reverse('fooodie:settingsprofilepic'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fooodie/loginregister.html')

    def test_settingspassword_view_status_200(self):
        response=self.client.get(reverse('fooodie:settingspassword'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fooodie/loginregister.html')
        
    def test_usersearch_view_status_200(self):
        response=self.client.get(reverse('fooodie:usersearch'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fooodie/error.html')
    
    def test_userprofile_view_status_200(self):
        response=self.client.get(reverse('fooodie:userprofile', args={'user_profile_slug': "randomstringfortesting"}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fooodie/profile.html')


    