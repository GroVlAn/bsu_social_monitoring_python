import json

from vk_api_app.handlers.vk_auth_handler import VkAuthHandler
from vk_api_app.handlers.vk_data_abstract_handler import VkDataAbstractHandler
from vk_api_app.json_models.vk_posts import PostResponse


class VkPostHandler(VkDataAbstractHandler):
    def __init__(self, vk_auth: VkAuthHandler):
        super().__init__(vk_auth=vk_auth)

    def get_posts(self, *, count: int = 100, offset: int = 0):
        posts = self._vk.wall.get(owner_id=-102554211, count=count, offset=offset)
        posts_json = json.dumps(posts)

        posts_object = PostResponse.parse_raw(posts_json)
        return posts_object
    