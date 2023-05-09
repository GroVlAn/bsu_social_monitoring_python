import json

from django.core.cache import cache
from django.http import HttpResponseBadRequest, JsonResponse

from django.urls import reverse_lazy
from django.views.generic import CreateView

from monitoring.forms.team_form import TeamForm
from monitoring.mixins import BaseMixin
from monitoring.models_db.team import Team


class TeamView(BaseMixin, CreateView):
    form_class = TeamForm
    title = 'Создание команды'
    template_name = 'pages/team/create/index.html'
    success_url = reverse_lazy('monitoring')

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.save(user=self.request.user)
        return super().form_valid(form)


class EditTeamView(BaseMixin, CreateView):
    form_class = TeamForm
    title = 'Изменение информации о команде'
    template_name = 'pages/team/edit/index.html'
    success_url = reverse_lazy('monitoring')

    def get_form_kwargs(self):
        kwargs = super(EditTeamView, self).get_form_kwargs()
        user = self.request.user
        team_key = f'{user.id}_{user.username}_team'
        team = cache.get(team_key)
        kwargs['team'] = team
        return kwargs

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = self.request.user
        team_key = f'{user.id}_{user.username}_team'
        team = cache.get(team_key)
        form.save(team=team, user=user)
        return super().form_valid(form)


def change_active_team(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    print(request.headers)
    if is_ajax:
        if request.method == 'POST':
            print(request.POST)
            data = json.load(request)
            team_id = data.get('team')
            team = Team.objects.get(pk=team_id)
            if not team:
                return JsonResponse({
                    'success': False,
                    'error': f'this Team: {team_id}, does not exits'
                }, status=200)
            team_key = f'{request.user.id}_{request.user.username}_team'
            cache.delete(team_key)
            cache.set(team_key, team)
            return JsonResponse({'success': True}, status=200)
    else:
        return HttpResponseBadRequest('Invalid request')
