from vk_api_app.handlers.vk_auth_handler import VkAuthHandler


class VkDataAbstractHandler:
    def __init__(self, *, vk_auth: VkAuthHandler):
        self._vk_auth = vk_auth
        self._vk = self._vk_auth.getVk()
