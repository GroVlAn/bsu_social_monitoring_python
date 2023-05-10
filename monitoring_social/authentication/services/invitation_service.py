from typing import Optional

from django.contrib.auth.models import User
from django.core.cache import cache
from rolepermissions.roles import assign_role

from authentication.models import Invitation
from monitoring.models_db.team import Team


class InvitationService:
    """Service for manipulate Invitation data"""

    @staticmethod
    def get_or_create_invitation(user: User, team: Team) -> Optional[Invitation]:
        if user is None:
            return None

        invitation = Invitation.objects.filter(user_id=user.id)
        print(len(tuple(invitation)))
        if len(tuple(invitation)) == 0:
            invitation = Invitation()
            invitation.user_id = user.id
            invitation.team_id = team.id
            invitation.save()
            print(invitation)
            return invitation

        return invitation[0]

    @staticmethod
    def add_used_to_team(user: User, uuid: str) -> None:
        invitation = Invitation.objects.get(UUID=uuid)
        team = Team.objects.get(pk=invitation.team_id)
        team.users.add(user)
        team.save()
        team_key = f'{user.id}_{user.username}_team'
        cache.set(team_key, team)
        assign_role(user, 'invited')
