from django.contrib import admin

from monitoring.models_db import AnalyzedItems
from monitoring.models_db.AnalyzedItems import GroupAnalyzedItems
from monitoring.models_db.Organization import Organization


admin.site.register(Organization)
admin.site.register(GroupAnalyzedItems)
prepopulated_fields = {'slug': {'name'}}
