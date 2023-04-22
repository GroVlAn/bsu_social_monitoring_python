from monitoring.services.organization_service import OrganizationService
from django.core.cache import cache


def generate_base_menu():
    return [
        {
            'name': 'Главная',
            'code': 'main',
            'url': '/monitoring',
            'active': False
        },
        {
            'name': 'Настройки',
            'code': 'settings',
            'url': '/settings',
            'active': False
        },
    ]


class BaseMixin:
    menu = generate_base_menu()
    title = 'Страница'
    active_menu = 0
    show_menu = True

    def get_base_context(self, *args, object_list=None, **kwargs):
        context = kwargs
        context['title'] = self.title
        context['active_menu'] = self.active_menu
        self.menu[self.active_menu]['active'] = True
        context['menu'] = self.menu
        if self.request.user:
            organization_key = f'{self.request.user.id}_{self.request.user.username}_organization'
            organizations = cache.get(organization_key) if cache.get(organization_key) is not None else None
            context['active_organization'] = organizations
            context['organizations'] = OrganizationService.get_all_organization(self.request.user)
        context['show_menu'] = self.show_menu
        return context
