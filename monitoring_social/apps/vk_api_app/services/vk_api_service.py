import datetime
import time
from enum import IntEnum

from typing import List

from apps.monitoring.models_db.search_items import SearchItem
from apps.monitoring.services.search_item_service import SearchItemService
from apps.monitoring.services.statistics_service import StatisticsService
from apps.vk_api_app.handlers.vk_handler import VkHandler
from apps.vk_api_app.handlers.vk_users_handler import VkUsersHandler
from apps.vk_api_app.models_db.vk_settings import VkSettings
from apps.vk_api_app.models_db.vk_user import VkUser
from apps.vk_api_app.handlers.redis_handler import RedisHandler
from apps.vk_api_app.handlers.vk_validation_handler import VkValidationHandler
from apps.vk_api_app.services._vk_api_post_service import VkAPIPostService
from apps.vk_api_app.services._vk_api_user_service import VkAPIUsersService
from apps.vk_api_app.services._vk_posts_service import VkPostsService
from apps.vk_api_app.services.vk_users_service import VkUsersService


class VkServiceType(IntEnum):
    POST = 0,
    USER = 1


class VkAPIService:
    _VK_APIS = (
        VkAPIPostService,
        VkAPIUsersService
    )

    def __init__(self, *,
                 redis_handler: RedisHandler,
                 vk_handler: VkHandler,
                 vk_validation: VkValidationHandler):
        self._redis_handler = redis_handler
        self._vk_handler = vk_handler
        self._vk_validation = vk_validation

    def create_service(self, *,
                       service_type: VkServiceType,
                       team_id: int = None,
                       search_items: List[SearchItem] = None):
        if service_type == VkServiceType.POST:
            return self._VK_APIS[service_type](
                redis_handler=self._redis_handler,
                vk_handler=self._vk_handler,
                vk_validation=self._vk_validation,
                search_items=search_items
            )
        elif service_type == VkServiceType.USER:
            return self._VK_APIS[service_type](
                redis_handler=self._redis_handler,
                team_id=team_id,
                vk_handler=self._vk_handler,
                vk_validation=self._vk_validation,
            )


class VkAPISummaryService:
    def __init__(self, *,
                 redis_handler: RedisHandler,
                 search_items: List[SearchItem],
                 vk_validation: VkValidationHandler):
        self._redis_handler = redis_handler
        self._search_items = search_items
        self._vk_validation = vk_validation

    def save_post_and_get_users(
            self,
            *,
            vk_api_posts_service: VkAPIPostService,
            vk_api_users_service: VkAPIUsersService,
            ids_posts: list) -> None:
        post_from_redis = self._redis_handler.get_posts_list(ids_list=ids_posts)
        for post in post_from_redis:
            vk_api_posts_service.save_post(post=post)
        for post_id in ids_posts:
            number_post_id = int(str(post_id).replace('post-', ''))
            vk_api_users_service.get_users(post_id=number_post_id)

    def count_likes(self, *, vk_users_handler: VkUsersHandler) -> None:
        for search_item in self._search_items:
            db_posts = VkPostsService.get_tuple_posts(search_item=search_item)
            search_item_key = f'search_item-{search_item.id}'

            for db_post in db_posts:
                users = vk_users_handler.getUsersIds(post_id=db_post.id_post)
                for user_id in users.ids:
                    db_user = VkUser.objects.filter(id_user=user_id).exists()

                    if db_user:
                        if self._redis_handler.is_key_exit(search_item_key):
                            self._redis_handler.update_single_value(key=search_item_key)
                        else:
                            self._save_json_search_likes(search_item_id=search_item.id)

                time.sleep(0.333)

    def save_search_items(self) -> None:
        for search_item in self._search_items:
            db_posts = VkPostsService.get_tuple_posts(search_item=search_item)
            statistic = {
                'likes': int(self._redis_handler.get_count_by_key(key=f'search_item-{search_item.id}')),
                'comments': sum([int(db_post.comments) for db_post in db_posts]),
                'reposts': sum([int(db_post.reposts) for db_post in db_posts]),
                'date_from': self._vk_validation.date_before,
                'date_to': self._vk_validation.date_after,
            }

            if StatisticsService.check_date(date=self._vk_validation.date_before, owner=search_item):
                StatisticsService.clear_statistics_by_owner(date=self._vk_validation.date_before, owner=search_item)

            StatisticsService.create(statistics=statistic, owner=search_item)

    def _save_json_search_likes(self, *, search_item_id: int) -> None:
        json_search_item = {
            'key': f'search_item-{search_item_id}',
            'value': 1
        }

        self._redis_handler.save_single_value(data=json_search_item)


def thread_worker(team):
    print('worker starting')
    time_start = time.monotonic()
    redis_handler = RedisHandler()
    redis_handler.clear_all()
    team_id = team.id
    vk_settings = VkSettings.objects.get(team=team)
    vk_validation = VkValidationHandler()
    if vk_settings is None:
        print('VKSettings is none')
        return

    search_items = list(SearchItem.objects.all().filter(team=team_id))
    vk_handler = VkHandler(token=vk_settings.token, group_id=vk_settings.group_id)
    vk_api = VkAPIService(
        redis_handler=redis_handler,
        vk_handler=vk_handler,
        vk_validation=vk_validation
    )
    vk_api_posts_service = vk_api.create_service(
        service_type=VkServiceType.POST,
        search_items=search_items
    )
    vk_api_users_service = vk_api.create_service(
        service_type=VkServiceType.USER,
        team_id=team_id
    )
    vk_api_service = VkAPISummaryService(redis_handler=redis_handler,
                                         search_items=search_items,
                                         vk_validation=vk_validation)

    def worker():
        vk_api_posts_service.get_posts()

        vk_api_service.save_post_and_get_users(
            vk_api_posts_service=vk_api_posts_service,
            vk_api_users_service=vk_api_users_service,
            ids_posts=vk_api_posts_service.ids_posts)

        vk_api_users_service.save_users(team=team)
        vk_api_service.count_likes(vk_users_handler=vk_api_users_service.vk_users_handler)
        vk_api_service.save_search_items()
        SearchItemService.count_summary(team=team)
        VkUsersService.count_summary(team)
        vk_api_users_service.save_users_info(team_id)
        time_end = time.monotonic()
        elapsed_time = datetime.timedelta(seconds=int(time_end - time_start))
        print('Task worked %s time' % elapsed_time)

    return worker
