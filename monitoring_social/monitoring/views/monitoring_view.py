import datetime

from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, TemplateView

from monitoring.forms.search_items_form import SearchItemsForm, GroupSearchItemsForm
from monitoring.mixins import BaseMixin
from monitoring.models_db.search_items import GroupSearchItems, SearchItem
from monitoring.models_db.team import Team
from monitoring.services.search_item_service import SearchItemService
from vk_api_app.models_db.vk_user import VkUser
from vk_api_app.services.vk_users_service import VkUsersService
from celery_app.tasks import start_get_data


class GroupSearchItemsFormView(BaseMixin, FormView):
    form_class = GroupSearchItemsForm
    title = 'Новая группа элементов'
    template_name = 'pages/monitoring/group/create/index.html'
    success_url = reverse_lazy('monitoring')

    def get_success_url(self):
        group_id = self.kwargs.get('id')
        if group_id is not None:
            return reverse_lazy('group_settings')
        return reverse_lazy('monitoring')

    def get_form_kwargs(self):
        kwargs = super(GroupSearchItemsFormView, self).get_form_kwargs()
        kwargs['request'] = self.request
        group_id = self.kwargs.get('id')
        if group_id is not None:
            group = GroupSearchItems.objects.get(pk=group_id)
            if group is not None:
                kwargs['group'] = group
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        group_id = self.kwargs.get('id')
        c_def['group_id'] = group_id
        if group_id is not None:
            self.success_url = reverse_lazy('group_settings')
        count = GroupSearchItems.objects.distinct().values('ru_name', 'team').count()
        print(count)
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        group_id = self.kwargs.get('id')
        if group_id is not None:
            group = GroupSearchItems.objects.get(pk=group_id)
            if group is not None:
                form.save(group=group)
                return super().form_valid(form)
        form.save()
        return super().form_valid(form)


class CreateSearchItem(BaseMixin, FormView):
    form_class = SearchItemsForm
    title = 'Новый элемент'
    template_name = 'pages/monitoring/create/index.html'
    success_url = reverse_lazy('monitoring')

    def get_success_url(self):
        group_id = self.kwargs.get('id')
        if group_id is not None:
            return reverse_lazy('search_items_settings')
        return reverse_lazy('monitoring')

    def get_form_kwargs(self):
        kwargs = super(CreateSearchItem, self).get_form_kwargs()
        kwargs['request'] = self.request
        search_item_id = self.kwargs.get('id')
        if search_item_id is not None:
            search_item = SearchItem.objects.get(pk=search_item_id)
            if search_item:
                kwargs['search_item'] = search_item
        return kwargs

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        search_item_id = self.kwargs.get('id')
        c_def['search_item_id'] = search_item_id
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        search_item_id = self.kwargs.get('id')
        if search_item_id is not None:
            search_item = SearchItem.objects.get(pk=search_item_id)
            if search_item is not None:
                form.save(search_item=search_item)
                return super().form_valid(form)
        form.save()
        return super().form_valid(form)


class MonitoringView(BaseMixin, TemplateView):
    title = 'Мониторинг'
    template_name = 'pages/monitoring/index.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        user = self.request.user
        team_key = f'{user.id}_{user.username}_team'
        current_team = cache.get(team_key)
        print(current_team)

        c_def['result'] = self.get_all_search_items(team=current_team)
        c_def['vk_users'] = VkUsersService.get_list(team=current_team)
        c_def['page_menu'] = self.make_monitoring_menu(team=current_team)
        return dict(list(context.items()) + list(c_def.items()))

    @staticmethod
    def make_monitoring_menu(*, team):
        grops = SearchItemService.get_all_groups_by_team(team=team)
        menu = [{'url': group.name, 'title': group.ru_name} for group in grops]
        menu.append({'url': '/vk/users', 'title': 'Пользователи'})
        return menu

    @staticmethod
    def get_all_search_items(*, team):
        groups = SearchItemService.get_all_groups_by_team(team=team)
        result = ({'name_group': group.ru_name,
                   'search_items': SearchItemService.get_list(
                       team=team,
                       name_grop=group.name)
                   } for group in groups)
        return result


class MonitoringVkUsersByDateView(BaseMixin, TemplateView):
    title = 'Пользователи Вконтакте по дате'
    template_name = 'pages/monitoring/detail/vk_users_date.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        user = self.request.user
        team_key = f'{user.id}_{user.username}_team'
        current_team = cache.get(team_key)
        date_from = datetime.datetime(2023, 4, 1)
        c_def['result'] = VkUsersService.get_all_by_date(
            team=current_team,
            date_from=date_from
        )
        return dict(list(context.items()) + list(c_def.items()))


class MonitoringVkUsersView(BaseMixin, ListView):
    model = VkUser
    title = 'Пользователи Вконтакте'
    template_name = 'pages/monitoring/detail/vk_users.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        user = self.request.user
        key_team = f'{user.id}_{user.username}_team'
        current_team = cache.get(key_team)
        c_def['vk_users'] = VkUsersService.get_list(team=current_team)
        return dict(list(context.items()) + list(c_def.items()))


class MonitoringDetailByDate(BaseMixin, TemplateView):
    title = 'Анализируемы элементы по дате'
    template_name = 'pages/monitoring/detail/date/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        group_slug = self.kwargs.get('group_slug')
        group_ru_name = GroupSearchItems.objects.get(name=group_slug).ru_name
        user = self.request.user
        team_key = f'{user.id}_{user.username}_team'
        current_team = cache.get(team_key)
        date_from = datetime.datetime(2023, 4, 1)
        search_items_result = SearchItemService.get_all_by_date(
            team=current_team,
            group_name=group_slug,
            date_from=date_from
        )
        filtered_search_items = filter(
            lambda ai: ai['search_item'].group.name == group_slug,
            search_items_result
        )
        c_def['result'] = {
            'name_group': group_ru_name,
            'analyzed_items': filtered_analyzed_items
        }
        return dict(list(context.items()) + list(c_def.items()))


class MonitoringDetailView(BaseMixin, ListView):
    model = GroupSearchItems
    title = 'Анализируемые элементы'
    template_name = 'pages/monitoring/detail/index.html'
    slug_field = 'monitoring_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_base_context(title=self.title)
        group = self.kwargs.get('group_slug')
        user = self.request.user
        key_team = f'{user.id}_{user.username}_team'
        current_team = cache.get(key_team)
        print(group)
        analyzed_items = SearchItemService.get_by_group(
            team=current_team,
            group=group
        )
        group_ru_name = GroupSearchItems.objects.get(name=group).ru_name

        c_def['result'] = {'name_group': group_ru_name,
                           'analyzed_items': analyzed_items}
        return dict(list(context.items()) + list(c_def.items()))


def start_getting_data_from_vk(request):
    if request.method == 'POST' and request.user.is_authenticated:
        team = Team.objects.get(users=request.user)
        start_get_data.delay({'team_id': team.id,
                              'user_id': request.user.id,
                              'user_name': request.user.username})
    return redirect('monitoring')
