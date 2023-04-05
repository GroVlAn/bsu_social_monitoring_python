from django.db import models
from django.utils import timezone
from monitoring.models_db.Organization import *


class GroupAnalyzedItems(models.Model):
    name = models.SlugField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Группа элементов'
    )
    ru_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Русское имя группы элементов'
    )
    level = models.IntegerField(default=1)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.ru_name

    class Meta:
        db_table = 'monitoring_group_analyzed_items'


class AnalyzedItem(models.Model):
    name = models.CharField(
        max_length=300,
        unique=True,
        verbose_name='Название анализируемого элемента'
    )
    description = models.TextField(null=True, verbose_name='Описание')
    date_create = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(GroupAnalyzedItems, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='analyzed_item'
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'monitoring_analyzed_item'


class AnalyzedItemsSummaryStatistics(models.Model):
    owner = models.OneToOneField(
        AnalyzedItem,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='summary_statistics'
    )
    likes = models.TextField(default=0)
    comments = models.TextField(default=0)
    reposts = models.TextField(default=0)
    score = models.IntegerField(default=0)

    class Meta:
        db_table = 'monitoring_analyzed_items_summary_statistics'


class AnalyzedItemKeywords(models.Model):
    keyword = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(AnalyzedItem, on_delete=models.CASCADE)

    class Meta:
        db_table = 'monitoring_analyzed_item_keywords'
