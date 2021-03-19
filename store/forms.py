from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Customer
class CreateUserForm(UserCreationForm):
    class Meta:
        model= User
        fields= ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

class CustomerForm(ModelForm):
    class Meta:
        model= Customer
        fields='__all__'
        exclude=['user']

class ChangeProfilePicture(ModelForm):
    class Meta:
        model= Customer
        fields=['profile_pic']