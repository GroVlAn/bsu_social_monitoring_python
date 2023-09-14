from django.urls import path

from apps.monitoring.views.main_view import index
from apps.monitoring.views.monitoring_view import (
    MonitoringView,
    MonitoringVkUsersView,
    MonitoringDetailView,
    start_getting_data_from_vk, CreateSearchItem, GroupSearchItemsFormView, MonitoringDetailByDate,
    MonitoringVkUsersByDateView)
from apps.monitoring.views.team_view import TeamView, change_active_team, EditTeamView
from apps.monitoring.views.settings_view import SettingsPage, UserSettingsView, SearchItemsSettingsView, GroupsSettingsView
from apps.vk_api_app.views import VkSettingsView


urlpatterns = [
    path('', index, name='home'),
    path('monitoring/team/create/', TeamView.as_view(), name='create_team'),
    path('settings/team/edit/', EditTeamView.as_view(), name='edit_team'),
    path('monitoring/', MonitoringView.as_view(), name='monitoring'),
    path('vk/users/', MonitoringVkUsersView.as_view(), name='vk_users'),
    path('vk/users/date/', MonitoringVkUsersByDateView.as_view(), name='vk_users_date'),
    path('monitoring/<slug:group_slug>', MonitoringDetailView.as_view(), name='monitoring_detail'),
    path('monitoring/date/<slug:group_slug>', MonitoringDetailByDate.as_view(), name='monitoring_detail_by_date'),
    path('vk/get/data', start_getting_data_from_vk, name='get_vk_api'),
    path('settings/', SettingsPage.as_view(), name='settings'),
    path('monitoring/create/', CreateSearchItem.as_view(), name='create_search_item'),
    path('monitoring/group/create/', GroupSearchItemsFormView.as_view(), name='group_search_items_form'),
    path('settings/user/', UserSettingsView.as_view(), name='user_settings'),
    path('settings/monitoring/items/', SearchItemsSettingsView.as_view(), name='search_items_settings'),
    path('settings/items/edit/<int:id>',
         CreateSearchItem.as_view(template_name='pages/monitoring/edit/templates/pages/monitoring/edit/index.html'), name='edit_search_item'),
    path('settings/groups/', GroupsSettingsView.as_view(), name='group_settings'),
    path('monitoring/team/active/change', change_active_team,
         name='team_active_change'),
    path('monitoring/grop/create/<int:id>',
         GroupSearchItemsFormView.as_view(template_name='pages/settings/monitoring/groups/edit/templates/pages/settings/monitoring/groups/edit/index.html'),
         name='edit_group_search_items'),
    path('settings/vk/', VkSettingsView.as_view(), name='vk_settings')
]
