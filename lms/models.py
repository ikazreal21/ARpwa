from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import locale
import uuid

from django.core.files.storage import FileSystemStorage
from django.db import models
from datetime import datetime


CATEGORY = (
        ("shapes", "Shapes"),
        ("colors", "Colors"),
        ("numbers", "Numbers"),
        ("alphabets", "Alphabets"),
    )


def create_rand_id():
        from django.utils.crypto import get_random_string
        return get_random_string(length=13, 
            allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')

class CustomUser(AbstractUser):
    GENDER = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, choices=GENDER, null=True, blank=True)
    birth_date = models.CharField(max_length=50, null=True, blank=True)
    # student_id = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='uploads/profile', blank=True, null=True)
    # total_points = models.IntegerField(default=0)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def date(self):
        try:
            # Convert the birth_date string to a datetime object
            date_obj = datetime.strptime(self.birth_date, "%Y-%m-%d")
            # Format it to 'Month day, Year' (e.g., 'September 21, 2024')
            return date_obj.strftime("%B %d, %Y")
        except ValueError:
            return self.birth_date


class ThreeDModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    marker = models.FileField(upload_to='uploads/markers', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/3dmodels', blank=True, null=True)
    threedfile = models.FileField(upload_to='uploads/3dmodels', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "3D Models"

class Quiz(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Quizzes"
    
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField()
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name_plural = "Questions"
    

class Record(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=CATEGORY)
    score = models.IntegerField()
    items = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category
    
    class Meta:
        verbose_name_plural = "Records"

class StudentRecord(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
    class Meta:
        verbose_name_plural = "Student Records"
