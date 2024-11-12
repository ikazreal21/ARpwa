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

    path('view_records/<str:pk>', views.view_records_list, name='view_records_list'),
    path('add-record/<str:pk>/<str:category>', views.AddRecord, name='add_record'),

    # Student Records
    path('alphabet_records/<str:pk>', views.AlphabetRecord, name='alphabet_records'),
    path('color_records/<str:pk>', views.ColorRecord, name='color_records'),
    path('shape_records/<str:pk>', views.ShapeRecord, name='shape_records'),
    path('number_records/<str:pk>', views.NumberRecord, name='number_records'),

    # 3D 
    path('arcamera/<str:pk>', views.arcamera, name='arcamera'),

    #AUTH
    path('login/', views.Login, name='login'),
    path('register/', views.Register, name='register'),
    path('logout/', views.Logout, name='logout'),

    # pwa
    url(r'^serviceworker\.js$', service_worker, name='serviceworker'),
    url(r'^manifest\.json$', manifest, name='manifest'),
    url('^offline/$', offline, name='offline'),

    path(".well-known/assetlinks.json", views.AssetLink),

    # Assesment
    path("assessment/<str:category>", views.Quizes, name='assessment'),
    path("questions/<str:quiz_id>", views.Questions, name='questions'),
    path("sumbit_assesment/<str:quiz_id>", views.SubmitQuiz, name='sumbit_assesment'),
] 