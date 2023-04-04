import json

from vk_api_app.handlers.vk_data_abstract_handler import VkDataAbstractHandler
from vk_api_app.json_models.vk_users import UserInfo, UsersId


def _to_json_item(item):
    vk_users_info_json = json.dumps(item)
    return UserInfo.parse_raw(vk_users_info_json)


class VkUsersHandler(VkDataAbstractHandler):

    def __init__(self, *, vk_auth):
        super().__init__(vk_auth=vk_auth)

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
