import vk_api


class VkAuthService:
    def __init__(self, *, token: str = None, group_id) -> None:
        self._vk_session = vk_api.VkApi(token=token)
        self._vk = self._vk_session.get_api()
        self.group_id = group_id

    def getVk(self):
        return self._vk
