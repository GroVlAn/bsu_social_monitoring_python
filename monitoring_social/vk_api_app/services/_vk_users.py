import json

from vk_api_app.services._vk_auth import VkAuth
from vk_api_app.json_models.vk_users import UsersId, UserInfo


def _to_json_item(item):
    vk_users_info_json = json.dumps(item)
    return UserInfo.parse_raw(vk_users_info_json)


class VkUsers:
    def __init__(self, vk_auth: VkAuth):
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
