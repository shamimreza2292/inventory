from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'employee_id', 'full_name', 'role', 'branch', 'phone_number', 'profile_image', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'employee_id', 'full_name', 'role', 'branch', 'phone_number', 'profile_image', 'email')
