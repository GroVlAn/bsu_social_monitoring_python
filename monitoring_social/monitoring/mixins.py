def generate_base_menu():
    return [
        {
            'name': 'Главная',
            'code': 'main',
            'url': ''
        },
        {
            'name': 'Мониторинг',
            'code': 'monitoring',
            'url': ''
        },
        {
            'name': 'Настройки',
            'code': 'settings',
            'url': ''
        },
    ]


class BaseMixin:
    menu = generate_base_menu()
    title = 'Страница'
    active_menu = 0
    show_menu = True

    def get_base_context(self, *args, object_list=None, **kwargs):
        context = kwargs
        context['menu'] = self.menu
        context['title'] = self.title
        context['active_menu'] = self.active_menu
        context['show_menu'] = self.show_menu
        return context
