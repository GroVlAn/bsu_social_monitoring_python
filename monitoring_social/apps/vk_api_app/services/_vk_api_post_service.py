import time
from typing import List

from apps.monitoring.models_db.search_items import SearchItem
from apps.monitoring.services.search_item_service import SearchItemService
from apps.vk_api_app.handlers.redis_handler import RedisHandler
from apps.vk_api_app.handlers.vk_handler import VkHandler, VkHandlerType
from apps.vk_api_app.handlers.vk_validation_handler import VkValidationHandler
from apps.vk_api_app.services._vk_api_abstract_service import VkAPIAbstractService
from apps.vk_api_app.services._vk_posts_service import VkPostsService


class VkAPIPostService(VkAPIAbstractService):

    def __init__(self, *,
                 redis_handler: RedisHandler,
                 vk_handler: VkHandler,
                 search_items: List[SearchItem],
                 vk_validation: VkValidationHandler):
        super().__init__(redis_handler=redis_handler, vk_handler=vk_handler, vk_validation=vk_validation)
        self._vk_posts_handler = self.vk_handler.create_handler(handler_type=VkHandlerType.POST)
        self._count_of_get_post = 100
        self._offset_of_get_post = 0
        self._search_items = search_items

    def get_posts(self) -> None:
        """
        Process is getting post from vk
        Function is getting post before post equal date from validation handler
        """
        while True:
            post_list = self._vk_posts_handler.get_posts(
                count=self._count_of_get_post,
                offset=self._offset_of_get_post)

            self._save_posts_ids_in_self(post_list=post_list.items)
            self._save_json_post(post_list=post_list.items)
            if not self._vk_validation.is_before_self_date(post_list.items[0].date):
                break
            else:
                self._refresh_counts_post()
                time.sleep(0.333)

    def _refresh_counts_post(self) -> None:
        self._offset_of_get_post += self._count_of_get_post

    def _save_posts_ids_in_self(self, *, post_list: list) -> None:
        self.ids_posts += [f'{post.prefix}{post.id}'
                           for post in post_list
                           if self._vk_validation.is_before_self_date(post.date)
                           and self._vk_validation.is_after_self_date(post.date)]

    def _save_json_post(self, *, post_list: list) -> None:
        json_post = [
            {
                'key': f'{post.prefix}{post.id}',
                'value': post.to_json()
            }
            for post in post_list
            if self._vk_validation.is_before_self_date(post.date) and self._vk_validation.is_after_self_date(post.date)
        ]
        self._redis_handler.save_key_value(json_post)

    def save_post(self, *, post: dict) -> None:
        for search_item in self._search_items:
            keywords = SearchItemService.get_keywords_tuple(search_item=search_item)
            if VkValidationHandler.text_contains_in_text_post(
                    current_text=post['text'],
                    searching_item=search_item.name) or \
                    (len(keywords) > 0 and
                     VkValidationHandler.keyword_in_text_post(current_text=post['text'], keywords=keywords)):
                VkPostsService.save_post(post=post, search_item=search_item)
