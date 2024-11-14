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
        'category': category
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
    assetlink = [{
      "relation": ["delegate_permission/common.handle_all_urls"],
      "target": {
        "namespace": "android_app",
        "package_name": "com.ellequin.scpar.twa",
        "sha256_cert_fingerprints": ["B7:49:13:A8:55:B8:00:20:D6:FD:51:95:20:98:FA:7F:E5:EF:4E:92:FF:9C:A4:63:7B:D2:ED:B3:91:47:14:24"]
      }
    }]

    return JsonResponse(assetlink, safe=False)



# Assessment
@login_required(login_url='login')
def Quizes(request, category):
    assesments = Quiz.objects.filter(category=category)
    context = {
        'quiz': assesments
    }
    return render(request, 'lms/quiz.html', context)

@login_required(login_url='login')
def Questions(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    all_questions = list(Question.objects.filter(quiz=quiz))
    selected_questions = sample(all_questions, int(quiz.number_of_items))
    
    request.session['multiplequestions_ids'] = [question.id for question in selected_questions]

    print(selected_questions)

    context = {
        'quiz': quiz,
        'multiple_choices': selected_questions
    }

    return render(request, 'lms/quizquestions.html', context)


@login_required(login_url='login')
def SubmitQuiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        correct_answers = 0
        total_questions = quiz.number_of_items

        # Retrieve question IDs from session
        question_ids = request.session.get('multiplequestions_ids', [])
        questions = Question.objects.filter(id__in=question_ids)

        # Check each submitted answer
        for question in questions:
            user_answer = request.POST.get(f'answer_{question.id}')
            print(f'Question {question.id}: {question.question} - User Answer: {user_answer} - Correct Answer: {question.answer}')
            if user_answer == question.answer:
                correct_answers += 1

        # Calculate score as a percentage
        score = (correct_answers / total_questions) * 100
        # earn_points = correct_answers * 0.05
        # user = request.user
        # user.save()
        
        # Save the result
        # Record.objects.create(
        #     user=request.user,
        #     quiz=quiz,
        #     score=earn_points,
        #     course_code=quiz.course.course_code
        # )
        
        return render(request, 'lms/quiz_results.html', {'quiz': quiz, 'score': score, "correct_answers" : correct_answers, "total_questions": total_questions})

    return redirect('assessment', category=quiz.category)
