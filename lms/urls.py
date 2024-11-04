from django.contrib.auth import views as auth_views
from django.urls import re_path as url

from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

from pwa.views import manifest, service_worker, offline



urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('categories/<str:category>', views.categories, name='categories'),
    path('records/', views.records_list, name='records_list'),
    path('student_records/', views.student_records, name='student_records'),
    path('add-record/', views.AddRecord, name='add_record'),

    # 3D 
    path('arcamera/<str:pk>', views.arcamera, name='arcamera'),

    #AUTH
    path('login/', views.Login, name='login'),
    path('register/', views.Register, name='register'),
    path('logout/', views.Logout, name='logout'),

    path('raw/<path:file_path>/', views.serve_raw_file, name='serve_raw_file'),
] 