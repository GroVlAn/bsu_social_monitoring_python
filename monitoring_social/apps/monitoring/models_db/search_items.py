from transliterate import translit

from django.utils import timezone
from django.utils.text import slugify

from apps.monitoring.models_db.team import *


class GroupSearchItems(models.Model):
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
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.ru_name

    def save(self, *args, **kwargs):
        if not self.name:
            slug_text = slugify(self.ru_name, allow_unicode=True)
            self.name = translit(slug_text, 'ru', reversed=True)

        super(GroupSearchItems, self).save(*args, **kwargs)

    class Meta:
        db_table = 'monitoring_group_search_items'


class SearchItem(models.Model):
    name = models.CharField(
        max_length=300,
        unique=True,
        verbose_name='Название анализируемого элемента'
    )
    description = models.TextField(null=True, verbose_name='Описание')
    time_create = models.DateTimeField(default=timezone.now)
    time_update = models.DateTimeField(default=timezone.now)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(GroupSearchItems, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='search_item'
    )

    def __str__(self):

        return self.name

    class Meta:
        db_table = 'monitoring_search_item'


class SearchItemsSummaryStatistics(models.Model):
    owner = models.OneToOneField(
        SearchItem,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='summary_statistics'
    )
    likes = models.TextField(default=0)
    comments = models.TextField(default=0)
    reposts = models.TextField(default=0)
    score = models.IntegerField(default=0)

    class Meta:
        db_table = 'monitoring_search_items_summary_statistics'


class SearchItemKeywords(models.Model):
    keyword = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(SearchItem, on_delete=models.CASCADE)

    class Meta:
        db_table = 'monitoring_search_item_keywords'
