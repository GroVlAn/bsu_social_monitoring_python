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
            'url': '#',
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
        context['show_menu'] = self.show_menu
        return context
