from django.shortcuts import redirect
from django.views.generic import CreateView

from monitoring.forms.organization_form import OrganizationForm
from monitoring.mixins import BaseMixin
from monitoring.services.organization_service import create_organization


class OrganizationView(BaseMixin, CreateView):
    form_class = OrganizationForm
    title = 'Создание организации'
    template_name = 'pages/organization/create/index.html'
    success_url = 'main'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        create_organization(self.request, form)
        return redirect('monitoring')