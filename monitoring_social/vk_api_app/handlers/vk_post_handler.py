import json

from vk_api.vk_api import VkApiMethod

from vk_api_app.json_models.vk_posts import PostResponse


class VkPostHandler:
    def __init__(self, *, vk: VkApiMethod, group_id: int):
        self._vk = vk
        self._group_id = group_id

    def get_posts(self, *, count: int = 100, offset: int = 0):
        posts = self._vk.wall.get(owner_id=-self._group_id, count=count, offset=offset)
        posts_json = json.dumps(posts)

        posts_object = PostResponse.parse_raw(posts_json)
        return posts_object
    