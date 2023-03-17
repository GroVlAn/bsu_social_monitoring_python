from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

INPUT_CLASS = 'auth__input'


class SignInForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Введён неправильный логин или пароль'
    }
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(
            attrs={'class': 'auth__input'}
        )
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'auth__input'}
        )
    )


class SignUpForm(UserCreationForm):
    error_messages = {
        'invalid': 'Такой аккаунт существует',
        'unique': 'Такой аккаунт существует',
        'password_mismatch': 'Пароль не совпадают',
    }

    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'auth__input'}),
        error_messages={
            'unique': "Пользователь с таким именем уже существует.",
            'required': "Это поле обязательно для заполнения.",
        },
    )
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'auth__input'})
    )
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'auth__input'})
    )
    middle_name = forms.CharField(
        label='Отчество',
        widget=forms.TextInput(attrs={'class': 'auth__input'})
    )
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'class': 'auth__input'})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'auth__input'}),
        error_messages={
            'invalid': 'Пароль не совпадают'
        }
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'auth__input'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'middle_name', 'email', 'password1', 'password2')
