from django.db import models
from monitoring.models_db.AnalyzedItems import *


class Statistics(models.Model):
    likes = models.TextField(default=0)
    comment = models.TextField(default=0)
    reports = models.TextField(default=0)
    owner = models.ForeignKey(
        AnalyzedItem,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'monitoring_statistics'
