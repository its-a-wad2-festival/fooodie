from django.test import SimpleTestCase
from django.urls import reverse, resolve
import fooodie.views
from fooodie.models import UserProfile, Photo, UserFactory

class TestUrls(SimpleTestCase):
    urls_views={'fooodie:home':views.home, 'fooodie:about':views.about,'fooodie:leaderboard':views.leaderboard,'fooodie:myprofile':views.myprofile,
    'fooodie:addfoodphoto':views.addfooodphoto, 'fooodie:settings':views.settings,'fooodie:deletepic':views.deletepic, 'fooodie:likephoto':views.likephoto
    'fooodie:settingspassword':views.settingspassword,'fooodie:settingsusername':views.settingsusername,'fooodie:settingsprofilepic':views.settingsprofilepic,
    'fooodie:settingsemail':views.settingsemail, 'fooodie:usersearch':views.usersearch,'fooodie:userprofile':views.userprofile, 'fooodie:logout':views.logout, 
    'fooodie:login':views.login,'fooodie:register':views.register, 'fooodie:loginregister':views.loginregister, 'fooodie:googleloggedin':views.googleloggedin}    
    def test_url_is_resolved(self, name):
        url=reverse(name)
        self.assertEquals(resolve(url).func, urls_views[name])