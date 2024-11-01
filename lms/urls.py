from django.contrib.auth import views as auth_views
from django.urls import re_path as url

from django.urls import path
from . import views

from pwa.views import manifest, service_worker, offline



urlpatterns = [
    path('', views.dashboard, name='dashboard'),



    #AUTH
    path('login/', views.Login, name='login'),
    path('register/', views.Register, name='register'),
    path('logout/', views.Logout, name='logout'),
]