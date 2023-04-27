from django.urls import path, reverse_lazy

from monitoring import views
from monitoring.views.main_view import index
from monitoring.views.monitoring_view import (
    MonitoringView,
    MonitoringVkUsers,
    MonitoringDetailView,
    start_getting_data_from_vk, CreateAnalyzedItem, GroupAnalyzedItemsFormView)
from monitoring.views.organization_view import OrganizationView, change_active_organization, EditOrganizationView
from monitoring.views.settings_view import SettingsPage, UserSettingsView, AnalyzedItemsSettingsView, GroupsSettingsView


urlpatterns = [
    path('', index, name='home'),
    path('monitoring/organization/create/', OrganizationView.as_view(), name='create_organization'),
    path('settings/organization/edit/', EditOrganizationView.as_view(), name='edit_organization'),
    path('monitoring/', MonitoringView.as_view(), name='monitoring'),
    path('vk/users/', MonitoringVkUsers.as_view(), name='vk_users'),
    path('monitoring/<slug:group_slug>', MonitoringDetailView.as_view(), name='monitoring_detail'),
    path('vk/get/data', start_getting_data_from_vk, name='get_vk_api'),
    path('settings/', SettingsPage.as_view(), name='settings'),
    path('monitoring/create/', CreateAnalyzedItem.as_view(), name='create_analyzed_item'),
    path('monitoring/grop/create/', GroupAnalyzedItemsFormView.as_view(), name='group_analyzed_items_form'),
    path('settings/user/', UserSettingsView.as_view(), name='user_settings'),
    path('settings/monitoring/items/', AnalyzedItemsSettingsView.as_view(), name='analyzed_items_settings'),
    path('settings/items/edit/<int:id>',
         CreateAnalyzedItem.as_view(template_name='pages/monitoring/edit/index.html'), name='edit_analyzed_item'),
    path('settings/groups/', GroupsSettingsView.as_view(), name='group_settings'),
    path('monitoring/organization/active/change', change_active_organization,
         name='organization_active_change'),
    path('monitoring/grop/create/<int:id>',
         GroupAnalyzedItemsFormView.as_view(template_name='pages/settings/monitoring/groups/edit/index.html'),
         name='edit_group_analyzed_items'),
]
