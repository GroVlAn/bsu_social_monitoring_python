from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, FormView

from authentication.forms import EditProfileForm
from monitoring.mixins import BaseMixin


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
            {'url': 'organization', 'title': 'Организация'},
            {'url': 'analyzed_items', 'title': 'Анализируемые элементы'},
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
