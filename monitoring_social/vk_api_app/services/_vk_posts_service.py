import json
import pytz
from datetime import datetime

from monitoring.models_db.AnalyzedItems import AnalyzedItem
from vk_api_app.json_models.vk_posts import PostResponse
from vk_api_app.models_db.vk_post import VkPost
from vk_api_app.services._vk_auth_service import VkAuthService


class VkPostsService:
    def __init__(self, *, vk_auth: VkAuthService) -> None:
        self._vk_auth = vk_auth
        self._vk = self._vk_auth.getVk()

    def get_posts(self, *, count: int = 100, offset: int = 0):
        posts = self._vk.wall.get(owner_id=-102554211, count=count, offset=offset)
        posts_json = json.dumps(posts)

        posts_object = PostResponse.parse_raw(posts_json)
        return posts_object

    @staticmethod
    def save_post(*, post: dict, analysed_item):
        exit_post = VkPost.objects.filter(id_post=post['id'], analysed_item=analysed_item).exists()
        if exit_post:
            return

        datetime_obj = datetime.fromtimestamp(post['date'])
        tz = pytz.timezone('Europe/Moscow')
        aware_datetime = tz.localize(datetime_obj)
        formatted_datetime = aware_datetime.strftime('%Y-%m-%d %H:%M:%S.%f%z')
        new_post = VkPost(
            id_post=post['id'],
            text=post['text'],
            date=formatted_datetime,
            likes=post['likes'],
            comments=post['comments'],
            reposts=post['reposts'],
            views=post['views'],
            analysed_item=analysed_item
        )
        new_post.save()

    @staticmethod
    def get_tuple_posts(*, analysed_item: AnalyzedItem) -> tuple:
        return tuple(VkPost.objects.filter(analysed_item=analysed_item)) or tuple()
