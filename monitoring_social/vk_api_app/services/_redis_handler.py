from datetime import datetime
import json

import redis


class RedisHandler:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=2)

    def __del__(self):
        self.redis_client.close()

    def save_key_value(self, data):
        """
        Save data in radis
        (data must be dictionary and contains key and value  keys of dictionary)
        """
        print(all(['key' in item or 'value' in item for item in data]))
        if not all(['key' in item or 'value' in item for item in data]):
            raise TypeError('Data must contains key and value')

        for item in data:
            self.redis_client.set(name=item['key'], value=item['value'])

        keys = self.redis_client.keys()
        for key in keys:
            last_item_date = self.redis_client.get(key)
            last_item_from_json = json.loads(last_item_date)
            print(datetime.fromtimestamp(last_item_from_json['date']))

    def clear_all(self):
        self.redis_client.flushdb()
        self.redis_client.flushall()
