from django.contrib.auth.models import User

from apps.monitoring.models_db.team import Team


class TeamService:

    @staticmethod
    def get_all_team(user: User):
        return Team.objects.filter(users=user)
