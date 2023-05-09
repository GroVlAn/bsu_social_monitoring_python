from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.core.cache import cache

from monitoring.models_db.team import Team
from .forms import *


class SignUpPage(CreateView):
    form_class = SignUpForm
    template_name = 'authentication/sign-up/index.html'
    success_url = reverse_lazy('monitoring')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect('monitoring')


class SignInPage(LoginView):
    form_class = SignInForm
    template_name = 'authentication/sign-in/index.html'

    def get_success_url(self):
        user = self.request.user
        team_key = f'{user.id}_{user.username}_team'
        team = Team.objects.filter(users=user).order_by('time_create')
        if team:
            cache.set(team_key, list(team)[0])
        return reverse_lazy('monitoring')


def logout_user(request):
    logout(request)
    return redirect('sign_in_page')
