from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from monitoring.forms.analyzed_items_form import AnalyzedItemsForm
from monitoring.mixins import BaseMixin
from monitoring.models_db import analyzed_items
from monitoring.models_db.analyzed_items import AnalyzedItem, GroupAnalyzedItems
from monitoring.models_db.organization import Organization
from monitoring.services.analysed_item_service import AnalyzedItemService
from monitoring.services.organization_service import create_analysed_item
from vk_api_app.models_db.vk_user import VkUser
from vk_api_app.services.vk_users_service import VkUsersService
from celery_app.tasks import start_get_data


class MonitoringView(BaseMixin, CreateView):
    form_class = AnalyzedItemsForm
    title = 'Мониторинг'
    template_name = 'monitoring/monitoring/index.html'
    success_url = 'main'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        c_def['result'] = self.get_all_analyzed_items()
        c_def['vk_users'] = VkUsersService.get_list(self.request.user)
        c_def['monitoring_menu'] = self.make_monitoring_menu()
        return dict(list(context.items()) + list(c_def.items()))

    def make_monitoring_menu(self):
        grops = AnalyzedItemService.get_all_groups()
        menu = [{'url': group.name, 'title': group.ru_name} for group in grops]
        return menu

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
        return redirect('monitoring')


class MonitoringVkUsers(BaseMixin, ListView):
    model = VkUser
    title = 'Пользователи Вконтакте'
    template_name = 'monitoring/monitoring/detail/vk_users.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        c_def['vk_users'] = VkUsersService.get_list(self.request.user)
        return dict(list(context.items()) + list(c_def.items()))


class MonitoringDetailView(BaseMixin, ListView):
    model = GroupAnalyzedItems
    title = 'Анализируемые элементы'
    template_name = 'monitoring/monitoring/detail/index.html'
    slug_field = 'monitoring_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        group = self.kwargs.get('monitoring_slug')
        analyzed_items = AnalyzedItemService.get_by_group(
            user=self.request.user,
            group=group
        )
        group_ru_name = GroupAnalyzedItems.objects.get(name=group).ru_name

        c_def['result'] = {'name_group': group_ru_name,
                           'analyzed_items': analyzed_items}
        return c_def


def start_getting_data_from_vk(request):
    if request.method == 'POST' and request.user.is_authenticated:
        organization = Organization.objects.get(users=request.user)
        start_get_data.delay({'organization_id': organization.id,
                              'user_id': request.user.id,
                              'user_name': request.user.username})
    return redirect('monitoring')
