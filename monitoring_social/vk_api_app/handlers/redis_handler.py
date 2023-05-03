from datetime import datetime
import json
from typing import Union

import redis

from vk_api_app.json_models.vk_posts import Post


class RedisHandler:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=2)

    def __del__(self):
        self.redis_client.close()

    def save_single_value(self, *, data: dict) -> None:
        if not ('key' in data or 'value' in data):
            raise TypeError('Data must contains key and value')

        self.redis_client.set(name=data['key'], value=data['value'])

    def update_single_value(self, *, key: str) -> None:
        current_value = int(self.redis_client.get(key))

        self.redis_client.set(name=key, value=current_value + 1)

    def save_key_value(self, data: list) -> None:
        """
        Save data in radis
        (data must be dictionary and contains key and value  keys of dictionary)
        """
        if not all(['key' in item or 'value' in item for item in data]):
            raise TypeError('Data must contains key and value')

        for item in data:
            value = json.dumps(item['value'])
            value_encode = value.encode('utf-8')
            self.redis_client.set(name=item['key'], value=value_encode)

    def is_key_exit(self, key: str) -> bool:
        return bool(self.redis_client.exists(key))

    def get_users(self) -> list[dict]:
        list_user_keys = list(self.redis_client.keys('user-*'))
        return [{'key': str(key).replace('b', '').replace("'", ''),
                 'count': int(self.redis_client.get(key))}
                for key in list_user_keys]

    def get_posts_list(self, *, ids_list: list) -> list[dict]:
        return [json.loads(self.redis_client.get(id_post).decode('utf-8')) for id_post in ids_list]

    def get_count_by_key(self, *, key: str) -> Union[str, int]:
        return self.redis_client.get(key) or 0

    def clear_all(self) -> None:
        self.redis_client.flushdb()
        self.redis_client.flushall()
