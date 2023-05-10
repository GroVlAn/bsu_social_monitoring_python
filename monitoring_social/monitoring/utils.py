from typing import Optional

from django.contrib.auth.models import User
from django.core.cache import cache

from monitoring.models_db.team import Team


def get_current_team(user: User) -> Optional[Team]:
    team_key = f'{user.id}_{user.username}_team'
    return cache.get(team_key)
