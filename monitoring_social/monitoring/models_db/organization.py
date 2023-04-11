from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Organization(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    time_create = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    users = models.ManyToManyField(
        User,
        blank=True,
    )

    def __str__(self):
        return self.name

    def to_json(self):
        return {'name': self.name}
