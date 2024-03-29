from django.db import models

from apps.monitoring.models_db.search_items import SearchItem


class Statistics(models.Model):
    likes = models.TextField(default=0)
    comments = models.TextField(default=0)
    reposts = models.TextField(default=0)
    date_from = models.DateTimeField(blank=True, null=True)
    date_to = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(
        SearchItem,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'monitoring_statistics'
