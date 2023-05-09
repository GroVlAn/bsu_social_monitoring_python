from django.db import models

from monitoring.models_db.team import Team


class VkSettings(models.Model):
    token = models.TextField(verbose_name='Токен авторизации vk')
    group_id = models.IntegerField(verbose_name='Id группы в vk')
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
