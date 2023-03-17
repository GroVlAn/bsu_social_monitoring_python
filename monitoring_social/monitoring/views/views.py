from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView

from monitoring.mixins import BaseMixin
from monitoring.services.OrganizationService import *

from monitoring.forms.OrganizationForm import OrganizationForm
from monitoring.forms.AnalyzedItemsForm import *


def index(request):
    return render(request, 'monitoring/index.html')


def main(request):
    return render(request, 'monitoring/main/index.html')


class Organization(BaseMixin, CreateView):
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
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(self.request)
        create_analysed_item(form)
        return redirect('main')
