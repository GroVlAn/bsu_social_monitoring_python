from django.contrib.auth.models import User
from django.db import models


class VkSettings(models.Model):
    token = models.TextField(verbose_name='Токен авторизации vk')
    group_id = models.IntegerField(verbose_name='Id группы в vk')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
