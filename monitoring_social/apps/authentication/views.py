from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView
from django.core.cache import cache

from apps.monitoring.mixins import BaseMixin
from apps.monitoring.models_db.team import Team
from apps.monitoring.utils import get_current_team
from .services.invitation_service import InvitationService
from .forms import *


class SignUpPage(CreateView):
    form_class = SignUpForm
    template_name = 'authentication/sign-up/index.html'
    success_url = reverse_lazy('monitoring')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uuid = self.request.GET.get('uuid')

        if uuid is not None:
            context['uuid'] = uuid

        return context

    def form_valid(self, form):
        user = form.save()
        uuid = self.request.POST.get('uuid')

        if uuid is not None:
            InvitationService.add_used_to_team(user=user, uuid=uuid)
        else:
            assign_role(user, 'owner')

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


class InviteUserView(BaseMixin, TemplateView):
    title = 'Пригласить пользователя'
    template_name = 'authentication/settings/invite/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        user = self.request.user
        current_team = get_current_team(user)
        invitation = InvitationService.get_or_create_invitation(user, current_team)
        if invitation is None:
            c_def['error'] = 'Не удалось создать ссылку для приглашения'
        else:
            domain = self.request.get_host()
            c_def['invited_link'] = f"{domain}{reverse('sign_up_page')}?uuid={invitation.UUID}"
        return dict(list(context.items()) + list(c_def.items()))
