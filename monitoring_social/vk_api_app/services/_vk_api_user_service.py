import time

from monitoring.models_db.team import Team
from vk_api_app.handlers.redis_handler import RedisHandler
from vk_api_app.handlers.vk_handler import VkHandler, VkHandlerType
from vk_api_app.handlers.vk_validation_handler import VkValidationHandler
from vk_api_app.json_models.vk_users import UsersId
from vk_api_app.models_db.vk_user import VkIgnoreUsers, VkUser
from vk_api_app.services._vk_api_abstract_service import VkAPIAbstractService
from vk_api_app.services._vk_user_statistics_service import VkUserStatisticsService
from vk_api_app.services.vk_users_service import VkUsersService


class VkAPIUsersService(VkAPIAbstractService):

    def __init__(self, *,
                 redis_handler: RedisHandler,
                 team_id: int,
                 vk_handler: VkHandler,
                 vk_validation: VkValidationHandler):
        super().__init__(redis_handler=redis_handler, vk_handler=vk_handler, vk_validation=vk_validation)
        self.vk_users_handler = self.vk_handler.create_handler(handler_type=VkHandlerType.USER)
        self._vk_ignore_users = list(VkIgnoreUsers.objects.all().filter(team=team_id))

    def get_users(self, *, post_id: int) -> None:
        vk_users = self.vk_users_handler.getUsersIds(post_id)

        for user_id in vk_users.ids:
            if not VkIgnoreUsers.objects.filter(id_user=user_id).exists():
                if self._redis_handler.is_key_exit(f'{vk_users.prefix}{user_id}'):
                    self._redis_handler.update_single_value(key=f'{vk_users.prefix}{user_id}')
                else:
                    self._save_json_user_id(vk_user=vk_users, user_id=user_id)

        time.sleep(0.333)

    def _save_json_user_id(self, *, vk_user: UsersId, user_id: int) -> None:
        json_user = {
            'key': f'{vk_user.prefix}{user_id}',
            'value': 1
        }

        self._redis_handler.save_single_value(data=json_user)

    def save_users(self, *, team: Team) -> None:
        users = self._redis_handler.get_users()

        for user in users:
            if user['count'] < 7:
                continue
            user_id = int(user['key'].replace('user-', ''))
            activity = user['count']
            if user_id not in [ignore_user.id for ignore_user in self._vk_ignore_users]:
                statistics = {
                    'date_from': self._vk_validation.date_before,
                    'date_to': self._vk_validation.date_after,
                    'activity': activity
                }

                if VkUserStatisticsService.check_date(date=self._vk_validation.date_before, owner_statistics=user_id):
                    VkUserStatisticsService.clear_vk_statistics_by_owner(
                        date=self._vk_validation.date_before,
                        owner_statistics=user_id)

                VkUserStatisticsService.create(statistics=statistics, owner=user_id, team=team)

    def save_users_info(self, team_id: int) -> None:
        users = VkUsersService.get_tuple_by_team(team_id=team_id)

        for user in users:
            user_id = user.id_user
            user_db = VkUser.objects.get(id_user=user_id)
            vk_user_info = self.vk_users_handler.getUserInfo(user_id)
            user_db.first_name = vk_user_info[0].first_name
            user_db.last_name = vk_user_info[0].last_name
            user_db.save()
            time.sleep(0.333)
