from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.monitoring.mixins import BaseMixin
from apps.vk_api_app.forms.vk_settings_form import VkSettingsForm
from apps.vk_api_app.models_db.vk_settings import VkSettings


class VkSettingsView(BaseMixin, CreateView):
    form_class = VkSettingsForm
    title = 'Настройка приложения Вконтакте'
    template_name = 'pages/settings/vk/index.html'
    success_url = reverse_lazy('monitoring')

    def get_vk_settings(self, request):
        user = self.request.user
        team_key = f'{user.id}_{user.username}_team'
        team = cache.get(team_key)

        try:
            return VkSettings.objects.get(team=team)
        except VkSettings.DoesNotExist:
            return None

    def get_form_kwargs(self):
        kwargs = super(VkSettingsView, self).get_form_kwargs()
        kwargs['request'] = self.request
        vk_settings = self.get_vk_settings(request=self.request)

        if vk_settings is not None:
            kwargs['vk_settings'] = vk_settings

        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)

        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        vk_settings = self.get_vk_settings(request=self.request)
        if vk_settings is not None:
            form.save(vk_settings=vk_settings)
            return super().form_valid(form)
        form.save()
        return super().form_valid(form)
