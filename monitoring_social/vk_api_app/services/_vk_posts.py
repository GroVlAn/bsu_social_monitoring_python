import json

from vk_api_app.json_models.vk_posts import PostResponse
from vk_api_app.services._vk_auth import VkAuth


class VkPosts:
    def __init__(self, *, vk_auth: VkAuth) -> None:
        self._vk_auth = vk_auth
        self._vk = self._vk_auth.getVk()

    def get_posts(self, *, count: int = 100, offset: int = 0):
        posts = self._vk.wall.get(owner_id=-102554211, count=count, offset=offset)
        posts_json = json.dumps(posts)

        posts_object = PostResponse.parse_raw(posts_json)
        return posts_object
