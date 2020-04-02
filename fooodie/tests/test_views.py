from django.test import TestCase, Client
from fooodie.models import UserProfile, Photo, UserFactory
from fooodie.views import *

#We test that views that do not need you to be signed have status code 200, and views that need you to log in, have status code 302
class ViewsTestCase(TestCase):
    def setup(self):
        self.client=Client()

    def test_home_view_status_200(self):
        client=Client()
        response=self.client.get(reverse('fooodie:home'))
        self.assertEquals(response.status_code, 200)
    
    def test_about_view_status_200(self):
        response=self.client.get(reverse('fooodie:about'))
        self.assertEquals(response.status_code, 200)

    def test_leaderboard_view_status_200(self):
        response=self.client.get(reverse('fooodie:leaderboard'))
        self.assertEquals(response.status_code, 200)

    def test_loginregister_view_status_200(self):
        response=self.client.get(reverse('fooodie:loginregister'))
        self.assertEquals(response.status_code, 200)

    def test_userlogin_view_status_200(self):
        response=self.client.get(reverse('fooodie:login'))
        self.assertEquals(response.status_code, 200)

    def test_register_view_status_200(self):
        response=self.client.get(reverse('fooodie:register'))
        self.assertEquals(response.status_code, 200)

    def test_userlogout_view_status_302(self):
        response=self.client.get(reverse('fooodie:logout'))
        self.assertEquals(response.status_code, 302)

    def test_addfoodphoto_view_status_302(self):
        response=self.client.get(reverse('fooodie:addfoodphoto'))
        self.assertEquals(response.status_code, 302)

    def test_deletepic_view_status_302(self):
        response=self.client.get(reverse('fooodie:deletepic', args={'user_profile_slug': 7}))
        self.assertEquals(response.status_code, 302)

    def test_myprofile_view_status_302(self):
        response=self.client.get(reverse('fooodie:myprofile'))
        self.assertEquals(response.status_code, 302)

    def test_settingsemail_view_status_302(self):
        response=self.client.get(reverse('fooodie:settingsemail'))
        self.assertEquals(response.status_code, 302)

    def test_settingsprofilepic_view_status_200(self):
        response=self.client.post(reverse('fooodie:settingsprofilepic'))
        self.assertEquals(response.status_code, 302)

    def test_settingspassword_view_status_302(self):
        response=self.client.get(reverse('fooodie:settingspassword'))
        self.assertEquals(response.status_code, 302)
        
    def test_usersearch_view_status_302(self):
        response=self.client.get(reverse('fooodie:usersearch'))
        self.assertEquals(response.status_code, 302)
    
    def test_userprofile_view_status_200(self):
        response=self.client.get(reverse('fooodie:userprofile', args={'user_profile_slug': "randomstringfortesting"}))
        self.assertEquals(response.status_code, 200)


    