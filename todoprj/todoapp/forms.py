from django import forms
from .models import todo
from django.db import models
from django.contrib.auth.models import User

class TodoForm(forms.ModelForm):
    class Meta:
        model = todo
        fields = ['todo_name', 'status']


class Event(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()

# class UserRegisrationForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
#         widgets = {
#             'password': forms.PasswordInput()
#         }