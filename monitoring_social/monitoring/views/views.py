from datetime import date

from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView

from monitoring.mixins import BaseMixin
from monitoring.models_db.Statistics import Statistics
from monitoring.services.analysed_item_service import AnalyzedItemService
from monitoring.services.organization_service import *

from monitoring.forms.OrganizationForm import OrganizationForm
from monitoring.forms.AnalyzedItemsForm import *
from vk_api_app.services._vk_users_service import VkUsersService
from vk_api_app.services.vk_api_service import start_get_data
from monitoring.models_db.Organization import Organization


def index(request):
    if request.user.is_authenticated:
        organization = Organization.objects.get(users=request.user)
        start_get_data(organization, request.user)
    return render(request, 'monitoring/index.html')


class OrganizationView(BaseMixin, CreateView):
    form_class = OrganizationForm
    title = 'Создание организации'
    template_name = 'monitoring/organization/create/index.html'
    success_url = 'main'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        create_organization(self.request, form)
        return redirect('main')


class Monitoring(BaseMixin, CreateView):
    form_class = AnalyzedItemsForm
    title = 'Мониторинг'
    template_name = 'monitoring/main/index.html'
    success_url = 'main'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        c_def['result'] = self.get_all_analyzed_items()
        print(VkUsersService.get_list(self.request.user)[0].vk_user_summary.score)
        c_def['vk_users'] = VkUsersService.get_list(self.request.user)
        return dict(list(context.items()) + list(c_def.items()))

    def get_all_analyzed_items(self):
        groups = AnalyzedItemService.get_all_groups()
        result = ({'name_group': group.ru_name,
                   'analyzed_items': AnalyzedItemService.get_list(
                       user=self.request.user,
                       name_grop=group.name)
                   } for group in groups)
        return result

    def form_valid(self, form):
        create_analysed_item(form)
        return redirect('main')
