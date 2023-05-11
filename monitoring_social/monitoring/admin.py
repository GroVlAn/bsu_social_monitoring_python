from django.contrib import admin

from monitoring.models_db import search_items
from monitoring.models_db.search_items import GroupSearchItems
from monitoring.models_db.team import Team


class GroupSearchItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'name': ('ru_name',)}


class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Team, TeamAdmin)
admin.site.register(GroupSearchItems, GroupSearchItemAdmin)
