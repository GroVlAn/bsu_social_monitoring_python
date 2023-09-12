from apps.monitoring.services.team_service import TeamService
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
            team_key = f'{self.request.user.id}_{self.request.user.username}_team'
            teams = cache.get(team_key) if cache.get(team_key) is not None else None
            context['active_team'] = teams
            context['teams'] = TeamService.get_all_team(self.request.user)
        context['show_menu'] = self.show_menu
        return context
