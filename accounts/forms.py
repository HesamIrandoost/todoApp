from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "full_name", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
