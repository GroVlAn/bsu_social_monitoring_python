from django.contrib.auth.models import User
from django.db import models


class VkUserStatistic(models.Model):
    activity = models.IntegerField()


class VkUser(models.Model):
    id_user = models.IntegerField()
    first_name = models.TextField()
    last_name = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    statistics = models.ForeignKey(VkUserStatistic, on_delete=models.CASCADE)

