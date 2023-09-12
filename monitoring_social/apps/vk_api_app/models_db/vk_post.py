from django.db import models

from apps.monitoring.models_db.search_items import SearchItem


class VkPost(models.Model):
    id_post = models.IntegerField(verbose_name='ID поста')
    text = models.TextField(blank=False, verbose_name='Текст поста')
    date = models.DateTimeField(blank=False, verbose_name='Дата публикации')
    likes = models.IntegerField(verbose_name='Количество лайков')
    comments = models.IntegerField(verbose_name='Количество комментариев')
    reposts = models.IntegerField(verbose_name='Количество "Поделиться"')
    views = models.IntegerField(verbose_name='Количество просмотров')
    search_item = models.ForeignKey(SearchItem, on_delete=models.CASCADE, blank=True, null=True)
    