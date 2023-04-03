import json

from monitoring.models_db.Organization import Organization
from vk_api_app.models_db.vk_user import VkUserStatistics, VkUser, VkUserSummaryStatistics
from vk_api_app.services._vk_auth_service import VkAuthService
from vk_api_app.json_models.vk_users import UsersId, UserInfo


def _to_json_item(item):
    vk_users_info_json = json.dumps(item)
    return UserInfo.parse_raw(vk_users_info_json)


class VkUsersService:
    def __init__(self, vk_auth: VkAuthService):
        self._vk_auth = vk_auth
        self._vk = self._vk_auth.getVk()

    def getUsersIds(self, post_id: int):
        vk_users_ids = self._vk.likes.getList(
            type='post',
            owner_id=-102554211,
            item_id=post_id)
        vk_users_ids_json = json.dumps(vk_users_ids)
        vk_users_ids_object = UsersId.parse_raw(vk_users_ids_json)

        return vk_users_ids_object

    def getUserInfo(self, user_id):
        vk_users_info = self._vk.users.get(
            type='post',
            owner_id=-102554211,
            user_ids=user_id,
            lang='RUS')
        vk_users_info_objects = [_to_json_item(item) for item in vk_users_info]

        return vk_users_info_objects

    @staticmethod
    def set_activity(*, activity: int) -> VkUserStatistics:
        activity = VkUserStatistics(activity=activity)
        activity.save()

        return activity

    @staticmethod
    def count_summary(organization: Organization) -> None:
        vk_users = tuple(VkUser.objects.filter(organization=organization))

        for vk_user in vk_users:
            vk_user_statistics = tuple(VkUserStatistics.objects.filter(owner=vk_user))
            if not VkUserSummaryStatistics.objects.filter(owner=vk_user).exists():
                vk_summary_statistic = VkUserSummaryStatistics(owner=vk_user)

                vk_summary_statistic.score = sum([int(vk_user_statistic.activity)
                                                  for vk_user_statistic in vk_user_statistics])

                vk_summary_statistic.save()
            else:
                vk_summary_statistic = VkUserSummaryStatistics.objects.get(owner=vk_user)

                vk_summary_statistic.score = sum([int(vk_user_statistic.activity)
                                                  for vk_user_statistic in vk_user_statistics])

                vk_summary_statistic.save()

    @staticmethod
    def get_list(user):
        organization = Organization.objects.get(users=user)
        return tuple(VkUser.objects.filter(organization=organization) \
                     .select_related('vk_user_summary').order_by('-vk_user_summary__score')[:10])
