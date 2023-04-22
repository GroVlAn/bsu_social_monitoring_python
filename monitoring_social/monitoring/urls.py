from django.urls import path

from monitoring import views
from monitoring.views.main_view import index
from monitoring.views.monitoring_view import (
    MonitoringView,
    MonitoringVkUsers,
    MonitoringDetailView,
    start_getting_data_from_vk, CreateAnalyzedItem, GroupAnalyzedItemsFormView)
from monitoring.views.organization_view import OrganizationView, change_active_organization
from monitoring.views.settings_view import SettingsPage, UserSettingsView


urlpatterns = [
    path('', index, name='home'),
    path('monitoring/organization/create/', OrganizationView.as_view(), name='create_organization'),
    path('monitoring/', MonitoringView.as_view(), name='monitoring'),
    path('vk/users/', MonitoringVkUsers.as_view(), name='vk_users'),
    path('monitoring/<slug:group_slug>', MonitoringDetailView.as_view(), name='monitoring_detail'),
    path('vk/get/data', start_getting_data_from_vk, name='get_vk_api'),
    path('settings/', SettingsPage.as_view(), name='settings'),
    path('monitoring/create/', CreateAnalyzedItem.as_view(), name='create_analyzed_item'),
    path('monitoring/grop/create/', GroupAnalyzedItemsFormView.as_view(), name='group_analyzed_items_form'),
    path('settings/user/', UserSettingsView.as_view(), name='user_settings'),
    path('monitoring/organization/active/change', change_active_organization,
         name='organization_active_change')
]
