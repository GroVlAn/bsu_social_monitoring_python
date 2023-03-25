import time
from threading import Thread

import redis
import json

from vk_api_app.services._redis_handler import RedisHandler
from vk_api_app.services._validation_vk_data import VkValidation
from vk_api_app.services._vk_auth import VkAuth
from vk_api_app.services._vk_posts import VkPosts


# token = 'af289c86af289c86af289c864fac3a9b8baaf28af289c86cc82b4b2eabdd842e60e7d76'
# vk_auth = VkAuth(token=token, group_id=-102554211)
#
# vk_posts = VkPosts(vk_auth=vk_auth)
#
# post_list = vk_posts.get_posts(count=100, offset=0)
#
# json_post = [{'id': post.id, 'value': json.dumps(post.to_json())} for post in post_list.items]
# print(json_post)
# redis_client = redis.Redis(host='localhost', port=6379, db=2)
#
# redis_client.flushdb()
# redis_client.flushall()
# # for post in json_post:
# #     redis_client.set(name=post['id'], value=post['value'])
# print(redis_client.keys())
#
# redis_client.close()


class VkAPIService:
    # TODO: удалить и заменить на получение с базы данных
    token = 'af289c86af289c86af289c864fac3a9b8baaf28af289c86cc82b4b2eabdd842e60e7d76'

    def __init__(self, *, redis_handler):
        vk_auth = VkAuth(token=self.token, group_id=-102554211)
        self.vk_posts = VkPosts(vk_auth=vk_auth)
        self.redis_handler = redis_handler
        self.ids_posts = []
        self.vk_validation = VkValidation()
        self.count_of_get_post = 100
        self.offset_of_get_post = 0

    def get_posts(self):
        while True:
            post_list = self.vk_posts.get_posts(
                count=self.count_of_get_post,
                offset=self.offset_of_get_post)
            self.ids_posts += [post.id for post in post_list.items]
            json_post = [
                {
                    'key': f'{post.prefix}{post.id}',
                    'value': json.dumps(post.to_json())
                }
                for post in post_list.items
                if self.vk_validation.is_before_self_date(post.date)
                and self.vk_validation.is_after_self_date(post.date)
            ]
            self.redis_handler.save_key_value(json_post)

            if not self.vk_validation.is_before_self_date(post_list.items[0].date):
                break
            else:
                self.refresh_counts_post()
                time.sleep(0.333)

    def refresh_counts_post(self):
        if self.count_of_get_post > 25:
            self.offset_of_get_post = self.count_of_get_post
            self.count_of_get_post //= 2
        else:
            self.offset_of_get_post += self.count_of_get_post


redis_handler = RedisHandler()
# redis_handler.clear_all()
vk_api_service = VkAPIService(redis_handler=redis_handler)
vk_api_service.get_posts()
