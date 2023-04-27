from django.contrib.auth.models import User
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, FormView

from authentication.forms import EditProfileForm
from monitoring.forms.analyzed_items_form import AnalyzedItemsForm
from monitoring.mixins import BaseMixin
from monitoring.models_db.analyzed_items import AnalyzedItem
from monitoring.services.analysed_item_service import AnalyzedItemService


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
            {'url': 'organization/edit/', 'title': 'Организация'},
            {'url': 'monitoring/items/', 'title': 'Анализируемые элементы'},
            {'url': 'groups/', 'title': 'Группы анализируемых элементов'}
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


class AnalyzedItemsSettingsView(BaseMixin, TemplateView):
    title = 'Настройки анализируемых элементов'
    template_name = 'pages/settings/monitoring/analysed_items/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        user = self.request.user
        organization_key = f'{user.id}_{user.username}_organization'
        current_organization = cache.get(organization_key)
        c_def['result'] = self.get_all_analyzed_items(organization=current_organization)
        return dict(list(context.items()) + list(c_def.items()))

    @staticmethod
    def get_all_analyzed_items(*, organization):
        groups = AnalyzedItemService.get_all_groups_by_organization(organization=organization)
        result = ({'group': group,
                   'analyzed_items': AnalyzedItemService.get_list(
                       organization=organization,
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
        organization_key = f'{user.id}_{user.username}_organization'
        organization = cache.get(organization_key)
        groups = AnalyzedItemService.get_all_groups_by_organization(organization)
        c_def['groups'] = groups
        return dict(list(context.items()) + list(c_def.items()))
