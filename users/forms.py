from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("email", "password1", "password2")  # Убрали username


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
