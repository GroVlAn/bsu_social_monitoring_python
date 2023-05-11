from django.contrib.auth.models import User

from monitoring.models_db.search_items import SearchItemsSummaryStatistics
from monitoring.models_db.team import Team


class TeamService:

    @staticmethod
    def get_all_team(user: User):
        return Team.objects.filter(users=user)
