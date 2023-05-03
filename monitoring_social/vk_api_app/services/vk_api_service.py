import datetime
import time
from enum import IntEnum

from typing import List

from monitoring.models_db.analyzed_items import AnalyzedItem
from monitoring.services.analysed_item_service import AnalyzedItemService
from monitoring.services.statistics_service import StatisticsService
from vk_api_app.handlers.vk_handler import VkHandler
from vk_api_app.handlers.vk_users_handler import VkUsersHandler
from vk_api_app.models_db.vk_settings import VkSettings
from vk_api_app.models_db.vk_user import VkUser
from vk_api_app.handlers.redis_handler import RedisHandler
from vk_api_app.handlers.vk_validation_handler import VkValidationHandler
from vk_api_app.services._vk_api_post_service import VkAPIPostService
from vk_api_app.services._vk_api_user_service import VkAPIUsersService
from vk_api_app.services._vk_posts_service import VkPostsService
from vk_api_app.services.vk_users_service import VkUsersService


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
                       organization_id: int = None,
                       analyzed_items: List[AnalyzedItem] = None):
        if service_type == VkServiceType.POST:
            return self._VK_APIS[service_type](
                redis_handler=self._redis_handler,
                vk_handler=self._vk_handler,
                vk_validation=self._vk_validation,
                analyzed_items=analyzed_items
            )
        elif service_type == VkServiceType.USER:
            return self._VK_APIS[service_type](
                redis_handler=self._redis_handler,
                organization_id=organization_id,
                vk_handler=self._vk_handler,
                vk_validation=self._vk_validation,
            )


class VkAPISummaryService:
    def __init__(self, *,
                 redis_handler: RedisHandler,
                 analyzed_items: List[AnalyzedItem],
                 vk_validation: VkValidationHandler):
        self._redis_handler = redis_handler
        self._analyzed_items = analyzed_items
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
        for analysed_item in self._analyzed_items:
            db_posts = VkPostsService.get_tuple_posts(analysed_item=analysed_item)
            analysed_item_key = f'analyzed_item-{analysed_item.id}'

            for db_post in db_posts:
                users = vk_users_handler.getUsersIds(post_id=db_post.id_post)
                for user_id in users.ids:
                    db_user = VkUser.objects.filter(id_user=user_id).exists()

                    if db_user:
                        if self._redis_handler.is_key_exit(analysed_item_key):
                            self._redis_handler.update_single_value(key=analysed_item_key)
                        else:
                            self._save_json_analysed_likes(analysed_item_id=analysed_item.id)

                time.sleep(0.333)

    def save_analyzed_items(self) -> None:
        for analyzed_item in self._analyzed_items:
            db_posts = VkPostsService.get_tuple_posts(analysed_item=analyzed_item)
            statistic = {
                'likes': int(self._redis_handler.get_count_by_key(key=f'analyzed_item-{analyzed_item.id}')),
                'comments': sum([int(db_post.comments) for db_post in db_posts]),
                'reposts': sum([int(db_post.reposts) for db_post in db_posts]),
                'date_from': self._vk_validation.date_before,
                'date_to': self._vk_validation.date_after,
            }

            if StatisticsService.check_date(date=self._vk_validation.date_before, owner=analyzed_item):
                StatisticsService.clear_statistics_by_owner(date=self._vk_validation.date_before, owner=analyzed_item)

            StatisticsService.create(statistics=statistic, owner=analyzed_item)

    def _save_json_analysed_likes(self, *, analysed_item_id: int) -> None:
        json_analysed_item = {
            'key': f'analyzed_item-{analysed_item_id}',
            'value': 1
        }

        self._redis_handler.save_single_value(data=json_analysed_item)


def thread_worker(organization):
    print('worker starting')
    time_start = time.monotonic()
    redis_handler = RedisHandler()
    redis_handler.clear_all()
    organization_id = organization.id
    vk_settings = VkSettings.objects.get(organization=organization)
    vk_validation = VkValidationHandler()
    if vk_settings is None:
        print('VKSettings is none')
        return

    analyzed_items = list(AnalyzedItem.objects.all().filter(organization=organization_id))
    vk_handler = VkHandler(token=vk_settings.token, group_id=vk_settings.group_id)
    vk_api = VkAPIService(
        redis_handler=redis_handler,
        vk_handler=vk_handler,
        vk_validation=vk_validation
    )
    vk_api_posts_service = vk_api.create_service(
        service_type=VkServiceType.POST,
        analyzed_items=analyzed_items
    )
    vk_api_users_service = vk_api.create_service(
        service_type=VkServiceType.USER,
        organization_id=organization_id
    )
    vk_api_service = VkAPISummaryService(redis_handler=redis_handler,
                                         analyzed_items=analyzed_items,
                                         vk_validation=vk_validation)

    def worker():
        vk_api_posts_service.get_posts()
        vk_api_service.save_post_and_get_users(
            vk_api_posts_service=vk_api_posts_service,
            vk_api_users_service=vk_api_users_service,
            ids_posts=vk_api_posts_service.ids_posts)
        vk_api_users_service.save_users(organization=organization)
        vk_api_service.count_likes(vk_users_handler=vk_api_users_service.vk_users_handler)
        vk_api_service.save_analyzed_items()
        AnalyzedItemService.count_summary(organization=organization)
        VkUsersService.count_summary(organization)
        vk_api_users_service.save_users_info(organization_id)
        time_end = time.monotonic()
        elapsed_time = datetime.timedelta(seconds=int(time_end - time_start))
        print('Task worked %s time' % elapsed_time)

    return worker
