import uuid

from django.db import models


class Invitation(models.Model):
    """Model for containing info about invite on link"""

    UUID = models.TextField(default=uuid.uuid4,
                            editable=False,
                            verbose_name='UUID ссылки для приглашения')
    user_id = models.IntegerField(verbose_name='ID пользователя')
    team_id = models.IntegerField(verbose_name='ID команды')
    date_create = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_invitation'

    def __str__(self):

        return f"UUID: {self.UUID}"
