from django.test import TestCase, Client
from fooodie.models import UserProfile, Photo, UserFactory
from fooodie.views import *

#We test that views that do not need you to be signed have status code 200, and views that need you to log in, have status code 200
class ViewsTestCaseWithoutLogIn(TestCase):
    def setup(self):
        self.client=Client()

    def test_home_view_status_200(self):
        client=Client()
        response=self.client.get(reverse('fooodie:home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fooodie/home.html')
        #We do not check for template as response should be an HTTP message to devs cause database was not populated.
    
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
        response=self.client.get(reverse('fooodie:login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fooodie/loginregister.html')

    def test_register_view_status_200(self):
        response=self.client.get(reverse('fooodie:register'))
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
        self.assertTemplateUsed(response, 'fooodie/profile.html')
    
    def test_userprofile_view_status_200(self):
        response=self.client.get(reverse('fooodie:userprofile', args={'user_profile_slug': "randomstringfortesting"}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'fooodie/profile.html')


    