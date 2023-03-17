class BaseMixin:
    menu = None
    title = 'Страница'
    active_menu = 0

    def get_base_context(self, *args, object_list=None, **kwargs):
        context = kwargs
        context['menu'] = self.menu
        context['title'] = self.title
        context['active_menu'] = self.active_menu
        return context
