import pytz
from datetime import datetime

from monitoring.models_db.search_items import SearchItem
from vk_api_app.models_db.vk_post import VkPost


class VkPostsService:

    @staticmethod
    def save_post(*, post: dict, search_item):
        exit_post = VkPost.objects.filter(id_post=post['id'], search_item=search_item).exists()
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
            search_item=search_item
        )
        new_post.save()

    @staticmethod
    def get_tuple_posts(*, search_item: SearchItem) -> tuple:
        return tuple(VkPost.objects.filter(search_item=search_item)) or tuple()
