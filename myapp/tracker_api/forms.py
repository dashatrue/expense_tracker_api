from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Обязательное поле')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)