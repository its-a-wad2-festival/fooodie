from django.urls import path
from fooodie import views

app_name='fooodie'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),]
"""path('add_photo/', views.add_photo, name='add_photo'),
path('user/<slug:user_name_slug>/', views.restricted, name='user'),
path('logout/', views.user_logout, name='logout'),"""

