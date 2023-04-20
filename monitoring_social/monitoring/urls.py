"""monitoring_social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from monitoring.views.main_view import index
from monitoring.views.monitoring_view import (
    MonitoringView,
    MonitoringVkUsers,
    MonitoringDetailView,
    start_getting_data_from_vk, CreateAnalyzedItem, GroupAnalyzedItemsFormView)
from monitoring.views.organization_view import OrganizationView
from monitoring.views.settings_view import SettingsPage, UserSettingsView


urlpatterns = [
    path('', index, name='home'),
    path('main/organization/create/', OrganizationView.as_view(), name='create_organization'),
    path('monitoring/', MonitoringView.as_view(), name='monitoring'),
    path('vk/users/', MonitoringVkUsers.as_view(), name='vk_users'),
    path('monitoring/<slug:monitoring_slug>', MonitoringDetailView.as_view(), name='monitoring_detail'),
    path('vk/get/data', start_getting_data_from_vk, name='get_vk_api'),
    path('settings/', SettingsPage.as_view(), name='settings'),
    path('monitoring/create/', CreateAnalyzedItem.as_view(), name='create_analyzed_item'),
    path('monitoring/grop/create/', GroupAnalyzedItemsFormView.as_view(), name='group_analyzed_items_form'),
    path('settings/user/', UserSettingsView.as_view(), name='user_settings')
]
