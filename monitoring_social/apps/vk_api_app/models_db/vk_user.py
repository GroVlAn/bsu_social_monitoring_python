from django.db import models

from apps.monitoring.models_db.team import Team


class VkUser(models.Model):
    id_user = models.IntegerField(unique=True)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class VkUserStatistics(models.Model):
    activity = models.IntegerField()
    date_from = models.DateTimeField(blank=True, null=True)
    date_to = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(
        VkUser,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'vk_user_statistic'


class VkIgnoreUsers(models.Model):
    id_user = models.IntegerField(unique=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class VkUserSummaryStatistics(models.Model):
    owner = models.OneToOneField(
        VkUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='vk_user_summary'
    )
    score = models.IntegerField()

    class Meta:
        db_table = 'vk_user_summary_statistics'
