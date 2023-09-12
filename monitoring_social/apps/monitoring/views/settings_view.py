from django.contrib.auth.models import User
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from apps.authentication.forms import EditProfileForm
from apps.monitoring.mixins import BaseMixin
from apps.monitoring.services.search_item_service import SearchItemService


class SettingsPage(BaseMixin, TemplateView):
    title = 'Настройки'
    template_name = 'pages/settings/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        c_def['page_menu'] = self.get_menu()
        return dict(list(context.items()) + list(c_def.items()))

    @staticmethod
    def get_menu():
        return [
            {'url': 'user', 'title': 'Пользователь'},
            {'url': 'team/edit/', 'title': 'Команда'},
            {'url': 'monitoring/items/', 'title': 'Искомые элементы'},
            {'url': 'groups/', 'title': 'Группы анализируемых элементов'},
            {'url': 'vk/', 'title': 'Настройки приложения Вконтакте'},
            {'url': 'invite/', 'title': 'Пригласить пользователя'},
        ]


class UserSettingsView(BaseMixin, FormView):
    model = User
    form_class = EditProfileForm
    title = 'Настройки пользователя'
    template_name = 'pages/settings/user/index.html'
    success_url = reverse_lazy('settings')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)

        return dict(list(context.items()) + list(c_def.items()))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)

    def get_initial(self):
        initial_data = super().get_initial()
        user = self.request.user
        initial_data['username'] = user.username
        initial_data['first_name'] = user.first_name
        initial_data['last_name'] = user.last_name
        initial_data['email'] = user.email

        return initial_data


class SearchItemsSettingsView(BaseMixin, TemplateView):
    title = 'Настройки анализируемых элементов'
    template_name = 'pages/settings/monitoring/search_items/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        user = self.request.user
        team_key = f'{user.id}_{user.username}_team'
        current_team = cache.get(team_key)
        c_def['result'] = self.get_all_search_items(team=current_team)
        return dict(list(context.items()) + list(c_def.items()))

    @staticmethod
    def get_all_search_items(*, team):
        groups = SearchItemService.get_all_groups_by_team(team=team)
        result = ({'group': group,
                   'search_items': SearchItemService.get_list(
                       team=team,
                       name_grop=group.name)
                   } for group in groups)
        return result


class GroupsSettingsView(BaseMixin, TemplateView):
    title = 'Группы анализируемых элементов'
    template_name = 'pages/settings/monitoring/groups/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        user = self.request.user
        team_key = f'{user.id}_{user.username}_team'
        team = cache.get(team_key)
        groups = SearchItemService.get_all_groups_by_team(team)
        c_def['groups'] = groups
        return dict(list(context.items()) + list(c_def.items()))
