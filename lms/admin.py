from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models
from django.contrib.auth.models import Group
from admin_interface.models import Theme

class UserAdminConfig(UserAdmin):
    model = CustomUser
    search_fields = ('username', 'email')
    list_filter = ('first_name', 'is_active', 'is_staff', 'gender', 'birth_date', 'is_teacher')
    list_display = ('username', 'id', 'email','is_active', 'is_staff', 'gender', 'birth_date', 'is_teacher')
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'username', 'email', 'password', 'gender', 'birth_date')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_teacher')}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})}
    }
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'first_name', 
                    'last_name',
                    'username',
                    'email',
                    'password1',
                    'password2',
                    'gender', 
                    'birth_date',
                    'image',
                    'is_active',
                    'is_staff',
                    'is_teacher'
                ),
            },
        ),
    )

admin.site.unregister(Group)
# admin.site.unregister(Theme)
admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(ThreeDModel)
admin.site.register(Quiz)
admin.site.register(Question)