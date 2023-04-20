from django.contrib import admin

from monitoring.models_db import analyzed_items
from monitoring.models_db.analyzed_items import GroupAnalyzedItems
from monitoring.models_db.organization import Organization


class GroupAnalyzedItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'name': ('ru_name',)}


admin.site.register(Organization)
admin.site.register(GroupAnalyzedItems, GroupAnalyzedItemAdmin)
