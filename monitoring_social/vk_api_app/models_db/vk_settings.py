from django.db import models

from monitoring.models_db.organization import Organization


class VkSettings(models.Model):
    token = models.TextField(verbose_name='Токен авторизации vk')
    group_id = models.IntegerField(verbose_name='Id группы в vk')
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
