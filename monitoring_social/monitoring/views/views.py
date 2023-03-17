from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView

from monitoring.mixins import BaseMixin
from monitoring.services.OrganizationService import *

from monitoring.forms.OrganizationForm import OrganizationForm


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

# def organization(request):
#     print(request.method == 'POST')
#     if request.method == 'POST':
#         form = OrganizationForm(request.POST)
#
#         if form.is_valid():
#             try:
#                 create_organization(request, form)
#                 return redirect('main')
#             except:
#                 form.add_error(None, 'Ошибка создания организации')
#     else:
#         form = OrganizationForm()
#     context = {
#         'title': 'Создание организации',
#         'form': form
#     }
#     return render(request, 'monitoring/organization/create/index.html', context)
