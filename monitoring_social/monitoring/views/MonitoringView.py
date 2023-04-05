from django.shortcuts import redirect
from django.views.generic import CreateView

from monitoring.forms.AnalyzedItemsForm import AnalyzedItemsForm
from monitoring.mixins import BaseMixin
from monitoring.models_db.Organization import Organization
from monitoring.services.analysed_item_service import AnalyzedItemService
from monitoring.services.organization_service import create_analysed_item
from vk_api_app.services.vk_users_service import VkUsersService
from celery_app.tasks import start_get_data


class Monitoring(BaseMixin, CreateView):
    form_class = AnalyzedItemsForm
    title = 'Мониторинг'
    template_name = 'monitoring/main/index.html'
    success_url = 'main'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        c_def['result'] = self.get_all_analyzed_items()
        c_def['vk_users'] = VkUsersService.get_list(self.request.user)
        return dict(list(context.items()) + list(c_def.items()))

    def make_monitoring_menu(self):
        grops = AnalyzedItemService.get_all_groups()

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


def start_getting_data_from_vk(request):
    if request.method == 'POST' and request.user.is_authenticated:
        organization = Organization.objects.get(users=request.user)
        print('YES')
        start_get_data.delay({'organization_id': organization.id,
                              'user_id': request.user.id,
                              'user_name': request.user.username})
    return redirect('main')
