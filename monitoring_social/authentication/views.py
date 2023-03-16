from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from .forms import *


class SignUpPage(CreateView):
    form_class = SignUpForm
    template_name = 'authentication/sign-up/index.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')


class SignInPage(LoginView):
    form_class = SignInForm
    template_name = 'authentication/sign-in/index.html'

    def get_success_url(self):
        return reverse_lazy('main')


def logout_user(request):
    logout(request)
    return redirect('sign_in_page')
