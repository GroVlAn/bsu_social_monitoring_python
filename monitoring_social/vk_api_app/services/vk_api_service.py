import datetime
import threading
import time
from monitoring.models_db.AnalyzedItems import AnalyzedItem
from monitoring.models_db.Organization import Organization
from monitoring.services.analysed_item_service import AnalyzedItemService
from monitoring.services.statistics_service import StatisticsService
from vk_api_app.handlers.vk_post_handler import VkPostHandler
from vk_api_app.handlers.vk_users_handler import VkUsersHandler
from vk_api_app.json_models.vk_users import UsersId
from vk_api_app.models_db.vk_user import VkUser, VkIgnoreUsers
from vk_api_app.handlers.redis_handler import RedisHandler
from vk_api_app.handlers.vk_validation_handler import VkValidationHandler
from vk_api_app.handlers.vk_auth_handler import VkAuthHandler
from vk_api_app.services._vk_posts_service import VkPostsService
from vk_api_app.services._vk_user_statistics_service import VkUserStatisticsService
from vk_api_app.services._vk_users_service import VkUsersService


class VkAPIAbstractService:
    # TODO: удалить и заменить на получение с базы данных
    token = 'af289c86af289c86af289c864fac3a9b8baaf28af289c86cc82b4b2eabdd842e60e7d76'

    def __init__(self, *, redis_handler, organization_id):
        self.vk_auth = VkAuthHandler(token=self.token, group_id=-102554211)
        self._vk_validation = VkValidationHandler()
        self._redis_handler = redis_handler
        self.ids_posts = []
        self._analyzed_items = list(AnalyzedItem.objects.all().filter(organization=organization_id))


class VkAPIPostService(VkAPIAbstractService):

    def __init__(self, *, redis_handler, organization_id):
        super().__init__(redis_handler=redis_handler, organization_id=organization_id)
        self._vk_posts_handler = VkPostHandler(vk_auth=self.vk_auth)
        self._count_of_get_post = 100
        self._offset_of_get_post = 0

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
        for analysed_item in self._analyzed_items:
            keywords = AnalyzedItemService.get_keywords_tuple(analysed_item=analysed_item)
            if VkValidationHandler.text_contains_in_text_post(
                    current_text=post['text'],
                    searching_item=analysed_item.name) or \
                    (len(keywords) > 0 and
                     VkValidationHandler.keyword_in_text_post(current_text=post['text'], keywords=keywords)):
                VkPostsService.save_post(post=post, analysed_item=analysed_item)


class VkAPIUsersService(VkAPIAbstractService):

    def __init__(self, *, redis_handler, organization_id):
        super().__init__(redis_handler=redis_handler, organization_id=organization_id)
        self.vk_users_handler = VkUsersHandler(vk_auth=self.vk_auth)
        self._vk_ignore_users = list(VkIgnoreUsers.objects.all().filter(organization=organization_id))

    def get_users(self, *, post_id: int) -> None:
        vk_users = self.vk_users_handler.getUsersIds(post_id)

        for user_id in vk_users.ids:
            if not VkIgnoreUsers.objects.filter(id_user=user_id).exists():
                if self._redis_handler.is_key_exit(f'{vk_users.prefix}{user_id}'):
                    self._redis_handler.update_single_value(key=f'{vk_users.prefix}{user_id}')
                else:
                    self._save_json_user_id(vk_user=vk_users, user_id=user_id)

        time.sleep(0.333)

    def _save_json_user_id(self, *, vk_user: UsersId, user_id: int) -> None:
        json_user = {
            'key': f'{vk_user.prefix}{user_id}',
            'value': 1
        }

        self._redis_handler.save_single_value(data=json_user)

    def save_users(self, *, organization: Organization) -> None:
        users = self._redis_handler.get_users()

        for user in users:
            if user['count'] < 7:
                continue
            user_id = int(user['key'].replace('user-', ''))
            activity = user['count']
            if user_id not in [ignore_user.id for ignore_user in self._vk_ignore_users]:
                statistics = {
                    'date_from': self._vk_validation.date_before,
                    'date_to': self._vk_validation.date_after,
                    'activity': activity
                }

                if VkUserStatisticsService.check_date(date=self._vk_validation.date_before, owner_statistics=user_id):
                    VkUserStatisticsService.clear_vk_statistics_by_owner(
                        date=self._vk_validation.date_before,
                        owner_statistics=user_id)

                VkUserStatisticsService.create(statistics=statistics, owner=user_id, organization=organization)

    def save_users_info(self, organization_id: int) -> None:
        users = VkUsersService.get_tuple_by_organization(organization_id=organization_id)

        for user in users:
            user_id = user.id_user
            user_db = VkUser.objects.get(id_user=user_id)
            vk_user_info = self.vk_users_handler.getUserInfo(user_id)
            user_db.first_name = vk_user_info[0].first_name
            user_db.last_name = vk_user_info[0].last_name
            user_db.save()
            time.sleep(0.333)


class VkAPIService(VkAPIAbstractService):
    def __init__(self, *, redis_handler, organization_id=15):
        super().__init__(redis_handler=redis_handler, organization_id=organization_id)

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
    time_start = time.time()
    redis_handler = RedisHandler()
    redis_handler.clear_all()
    vk_api_posts_service = VkAPIPostService(redis_handler=redis_handler, organization_id=organization.id)
    vk_api_users_service = VkAPIUsersService(redis_handler=redis_handler, organization_id=organization.id)
    vk_api_service = VkAPIService(redis_handler=redis_handler, organization_id=organization.id)

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
        vk_api_users_service.save_users_info(organization.id)
        time_end = time.time()
        elapsed_time = datetime.timedelta(seconds=int(time_end - time_start))
        print('thread worked %s time' % elapsed_time)

    return worker


def start_get_data(organization, user):
    id_thread = str(user.id) + user.username
    if id_thread not in [thread.name for thread in threading.enumerate()]:
        worker = thread_worker(organization)
        thread = threading.Thread(target=worker, name=id_thread)
        thread.start()
