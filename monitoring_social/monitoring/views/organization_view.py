import json

from django.core.cache import cache
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from monitoring.forms.organization_form import OrganizationForm
from monitoring.mixins import BaseMixin
from monitoring.models_db.organization import Organization


class OrganizationView(BaseMixin, CreateView):
    form_class = OrganizationForm
    title = 'Создание организации'
    template_name = 'pages/organization/create/index.html'
    success_url = reverse_lazy('monitoring')

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.save(user=self.request.user)
        return super().form_valid(form)


class EditOrganizationView(BaseMixin, CreateView):
    form_class = OrganizationForm
    title = 'Изменение организации'
    template_name = 'pages/organization/edit/index.html'
    success_url = reverse_lazy('monitoring')

    def get_form_kwargs(self):
        kwargs = super(EditOrganizationView, self).get_form_kwargs()
        user = self.request.user
        organization_key = f'{user.id}_{user.username}_organization'
        organization = cache.get(organization_key)
        kwargs['organization'] = organization
        return kwargs

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = self.request.user
        organization_key = f'{user.id}_{user.username}_organization'
        organization = cache.get(organization_key)
        form.save(organization=organization, user=user)
        return super().form_valid(form)


def change_active_organization(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    print(request.headers)
    if is_ajax:
        if request.method == 'POST':
            print(request.POST)
            data = json.load(request)
            organization_id = data.get('organization')
            organization = Organization.objects.get(pk=organization_id)
            if not organization:
                return JsonResponse({
                    'success': False,
                    'error': f'this Organization: {organization_id}, does not exits'
                }, status=200)
            organization_key = f'{request.user.id}_{request.user.username}_organization'
            cache.delete(organization_key)
            cache.set(organization_key, organization)
            return JsonResponse({'success': True}, status=200)
    else:
        return HttpResponseBadRequest('Invalid request')
