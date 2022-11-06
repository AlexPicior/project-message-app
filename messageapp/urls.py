"""messageapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from sqlite3 import paramstyle
from django.contrib import admin
from django.urls import path, include
from signin_signup_sys import views as v0
from home import views as v1

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign_up/', v0.sign_up, name='sign_up'),
    path('friend/', include('friend.urls', namespace='friend')),
    path('message/', include('message.urls', namespace='message')),
    path('', v1.home, name='home'),
    path('', include('django.contrib.auth.urls')),
    path('', include('user_home.urls')),
]
