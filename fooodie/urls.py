from django.urls import path
from fooodie import views
from django.conf.urls import url

app_name='fooodie'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('leaderboard/', views.leaderboard, name = 'leaderboard'),

    path('myprofile/', views.myprofile, name = 'myprofile'),
    path('myprofile/addfoodphoto/', views.addfoodphoto, name = 'addfoodphoto'),
    path('myprofile/settings/', views.usersettings, name = 'settings'),
    path('myprofile/settings/deletepic/<slug:photo_id>/', views.deletepic, name = 'deletepic'),
    url(r'^password/$', views.settingspassword, name='settingspassword'),
    path('myprofile/settings/username/', views.settingsusername, name = 'settingsusername'),
    path('myprofile/settings/profilepic/', views.settingsprofilepic, name = 'settingsprofilepic'),
    path('myprofile/settings/email/', views.settingsemail, name = 'settingsemail'),
    path('myprofile/settings/deleteaccount', views.deleteaccount, name='deleteaccount'),

    path('usersearch/', views.usersearch, name='usersearch'),
    path('user/<slug:user_profile_slug>/', views.userprofile, name='userprofile'),

    path('logout/', views.userlogout, name='logout'),
    path('login/', views.userlogin, name='login'),
    path('register/', views.register, name = 'register'),
    path('loginregister/', views.loginregister, name='loginregister'),
    path('googleloggedin/', views.googleloggedin, name='googleloggedin'),


    path('like_photo/', views.LikePhoto.as_view(), name = 'likephoto'),
    ]
