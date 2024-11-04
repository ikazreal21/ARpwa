from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelForm, ValidationError
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2"]


class ThreeDModelForm(ModelForm):
    class Meta:
        model = ThreeDModel
        fields = ['name', 'description', 'image', 'threedfile', 'marker']


class RecordForm(ModelForm):
    class Meta:
        model = Record
        fields = '__all__'
