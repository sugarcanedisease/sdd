from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1', 'password2']
        widgets = {
            'username' : forms.TextInput(attrs = {'placeholder': 'Enter Username'}),
            'password1' : forms.PasswordInput(attrs = {'placeholder': 'Enter Password'}),
            'password2' : forms.PasswordInput(attrs = {'placeholder': 'Confirm Password'}),
            'email' : forms.EmailInput(attrs = {'placeholder': 'Enter Email'}),
        }
        
        # fields = "__all__"