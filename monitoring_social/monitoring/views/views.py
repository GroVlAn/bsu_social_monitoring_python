from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView

from monitoring.mixins import BaseMixin
from monitoring.services.organization_service import *

from monitoring.forms.OrganizationForm import OrganizationForm
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


