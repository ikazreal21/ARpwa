from django.contrib.auth import views as auth_views
from django.urls import re_path as url

from django.urls import path
from . import views

from pwa.views import manifest, service_worker, offline



urlpatterns = []