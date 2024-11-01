from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import locale
import uuid

from django.core.files.storage import FileSystemStorage
from django.db import models
from datetime import datetime


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
