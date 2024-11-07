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

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'lms/index.html')

@login_required(login_url='login')
def categories(request, category):
    threedModel = ThreeDModel.objects.filter(category=category)
    context = {
        'threedModel': threedModel,
    }
    return render(request, 'lms/categories.html', context)

@login_required(login_url='login')
def records_list(request):
    records = StudentRecord.objects.all()
    return render(request, 'lms/records_list.html', {'records': records})

@login_required(login_url='login')
def AlphabetRecord(request, pk):
    student = StudentRecord.objects.get(id=pk)
    records_list = Record.objects.filter(student_id=student.student_id, category='alphabets')
    context = {'records_list': records_list, 'pk': pk}
    return render(request, 'lms/student_alphabet.html', context)

@login_required(login_url='login')
def ColorRecord(request, pk):
    student = StudentRecord.objects.get(id=pk)
    records_list = Record.objects.filter(student_id=student.student_id, category='colors')
    context = {'records_list': records_list, 'pk': pk}
    return render(request, 'lms/student_color.html', context)

@login_required(login_url='login')
def ShapeRecord(request, pk):
    student = StudentRecord.objects.get(id=pk)
    records_list = Record.objects.filter(student_id=student.student_id, category='shapes')
    context = {'records_list': records_list, 'pk': pk}
    return render(request, 'lms/student_shape.html', context)

@login_required(login_url='login')
def NumberRecord(request, pk):
    student = StudentRecord.objects.get(id=pk)
    records_list = Record.objects.filter(student_id=student.student_id, category='numbers')
    context = {'records_list': records_list, 'pk': pk}
    return render(request, 'lms/student_numbers.html', context)

@login_required(login_url='login')
def view_records_list(request, pk):
    context = {'pk': pk}
    return render(request, 'lms/student_records.html', context)

@login_required(login_url='login')
def AddRecord(request, pk, category):
    student = StudentRecord.objects.get(id=pk)
    form = RecordForm()
    if request.method == 'POST':
        date = request.POST.get("date")
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save(commit=False).user = request.user
            record = form.save()
            record.student_id = student.student_id
            record.category = category
            record.assesment_date = date
            record.save()
            if category == 'alphabets':
                return redirect('alphabet_records', pk=pk)
            elif category == 'colors':
                return redirect('color_records', pk=pk)
            elif category == 'numbers':
                return redirect('shape_records', pk=pk)
            elif category == 'shapes':
                return redirect('number_records', pk=pk)
        print(form.errors)
    return render(request, 'lms/add_record.html', {'form': form})

# 3D
@login_required(login_url='login')
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
        print(user)
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


# PWA

def AssetLink(request):
    assetlink = [
        {
            "relation": ["delegate_permission/common.handle_all_urls"],
            "target": {
            "namespace": "android_app",
            "package_name": "xyz.appmaker.yiwvwg",
            "sha256_cert_fingerprints": ["75:44:B1:7B:3C:AA:A1:67:DC:44:B8:F5:6B:F6:D6:2D:10:4C:7F:20:BC:05:E2:FC:44:96:22:07:AD:1F:A6:6B"]
            }
        }
    ]

    return JsonResponse(assetlink, safe=False)