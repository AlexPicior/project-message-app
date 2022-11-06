from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.user_home, name='user_home'),
    path('home/friends', views.friends, name='friends'),
    path('home/notifications', views.notifications, name='notifications'),
    path('home/add_friend', views.add_friend, name='add_friend'),
]
