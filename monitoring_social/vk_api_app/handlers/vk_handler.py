from enum import IntEnum

import vk_api

from vk_api_app.handlers.vk_post_handler import VkPostHandler
from vk_api_app.handlers.vk_users_handler import VkUsersHandler


class VkHandlerType(IntEnum):
    POST = 0
    USER = 1
    VALIDATION = 2


class VkHandler:
    _VK_HANDLERS = (
        VkPostHandler,
        VkUsersHandler
    )

    def __init__(self, *, token: str, group_id: int):
        self._vk_session = vk_api.VkApi(token=token)
        self._vk = self._vk_session.get_api()
        self._group_id = group_id

    def create_handler(self, *, handler_type: VkHandlerType):
        return self._VK_HANDLERS[handler_type](vk=self._vk, group_id=self._group_id)
