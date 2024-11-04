from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from .forms import *
from .models import *
# from .utils import *

from django.db.models import Q


from django.http import FileResponse

import time
from random import sample

from django.db.models import Sum, F

from django.http import HttpResponse, Http404
import requests

import os
from django.conf import settings

# @login_required(login_url='login')
def dashboard(request):
    return render(request, 'lms/index.html')

def categories(request, category):
    threedModel = ThreeDModel.objects.filter(category=category)
    context = {
        'threedModel': threedModel,
    }
    return render(request, 'lms/categories.html', context)

def records_list(request):
    records = Record.objects.all()
    return render(request, 'lms/records_list.html', {'records': records})

def student_records(request):
    records = Record.objects.filter(user=request.user)
    return render(request, 'lms/student_records.html', {'records': records})

def AddRecord(request):
    form = RecordForm()
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('records_list')
    return render(request, 'lms/record_form.html', {'form': form})

# 3D
def arcamera(request, pk):
    model = ThreeDModel.objects.get(id=pk)
    # Render the AR viewer page, passing the absolute proxy URL
    return render(request, 'lms/arcamera.html', {'model': model})

# AUTH
def Login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next', 'dashboard')
            return redirect(next_url)
            # return redirect('dashboard')
        else:
            messages.error(request, 'Username or Password is incorrect')
    return render(request, 'lms/login.html', {'next': request.GET.get('next', '')})

def Register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_student = True
            user.save()
            return redirect('login')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'lms/register.html')

def Logout(request):
    logout(request)
    return redirect('login')