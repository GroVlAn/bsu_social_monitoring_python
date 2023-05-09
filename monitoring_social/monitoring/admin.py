from django.contrib import admin

from monitoring.models_db import analyzed_items
from monitoring.models_db.analyzed_items import GroupAnalyzedItems
from monitoring.models_db.team import Team


class GroupAnalyzedItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'name': ('ru_name',)}


class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Team, TeamAdmin)
admin.site.register(GroupAnalyzedItems, GroupAnalyzedItemAdmin)
