from django.shortcuts import render, redirect
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

# @login_required(login_url='login')
def dashboard(request):
    return render(request, 'lms/index.html')

# AUTH
def Login(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            return redirect('dashboard')
        else:
            return redirect('teacher_dashboard')
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