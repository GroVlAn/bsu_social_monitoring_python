from django.db import models

from monitoring.models_db.AnalyzedItems import AnalyzedItem


class VkPost(models.Model):
    id_post = models.IntegerField(verbose_name='ID поста')
    text = models.TextField(blank=False, verbose_name='Текст поста')
    date = models.DateTimeField(blank=False, verbose_name='Дата публикации')
    likes = models.IntegerField(verbose_name='Количество лайков')
    comments = models.IntegerField(verbose_name='Количество комментариев')
    reposts = models.IntegerField(verbose_name='Количество "Поделиться"')
    views = models.IntegerField(verbose_name='Количество просмотров')
    analysed_item = models.ForeignKey(AnalyzedItem, on_delete=models.CASCADE, blank=False)
    