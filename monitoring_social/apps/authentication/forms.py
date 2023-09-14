from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
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
        fields = ('username', 'last_name', 'first_name', 'email', 'password1', 'password2')

    def save(self, commit=True):

        user = super().save(commit=False)

        if commit:
            user.save()

        return user


class EditProfileForm(UserChangeForm):
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(),
        required=False
    )
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(),
        required=False
    )
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput()
    )
    password = forms.CharField(
        label='Старый пароль',
        widget=forms.PasswordInput(),
        required=False
    )
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(),
        required=False
    )

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email'
        )

    def clean(self):

        cleaned_data = super().clean()

        old_password = cleaned_data.get('password')

        if not old_password:
            return cleaned_data

        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        user = authenticate(username=self.instance.username, password=old_password)

        if user is None:
            raise forms.ValidationError('Старый пароль указан неверно')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError('Новые пароль не совпадают')

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('new_password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user
