import json
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
from typing import List, Optional

from vk_api import *
from pydantic import BaseModel


class CountableValue(BaseModel):
    count: int


class Post(BaseModel):
    id: int
    date: int
    text: str
    comments: Optional[CountableValue]
    likes: Optional[CountableValue]
    repost: Optional[CountableValue]
    views: Optional[CountableValue]

    def __str__(self):
        string = '{\n'
        for key in vars(self):
            string += f'\t{key}: {getattr(self, key)}\n'
        else:
            string += '}'
        return string


class PostResponse(BaseModel):
    items: List[Post]

    def __str__(self):
        string = '{\n'
        for item in self.items:
            string += f'{item}\n'
        else:
            string += '}'
        return string


class UsersId(BaseModel):
    ids: List[int] = []

    class Config:
        fields = {
            'ids': 'items'
        }


class UserInfo(BaseModel):
    id: int
    first_name: str
    last_name: str


vk_session = vk_api.VkApi(token='af289c86af289c86af289c864fac3a9b8baaf28af289c86cc82b4b2eabdd842e60e7d76')
vk = vk_session.get_api()

posts = vk.wall.get(owner_id=-102554211, count=1)
posts_json = json.dumps(posts)

posts_object = PostResponse.parse_raw(posts_json)

vk_users = vk.likes.getList(type='post', owner_id=-102554211, item_id=posts_object.items[0].id)
users_id_json = json.dumps(vk_users)
users_id_object = UsersId.parse_raw(users_id_json)

print(users_id_object)

vk_users_info = vk.users.get(type='post', owner_id=-102554211, user_ids=users_id_object.ids[0], lang='RUS')
vk_users_info_json = json.dumps(vk_users_info[0])
vk_users_info_object = UserInfo.parse_raw(vk_users_info_json)
print(vk_users_info_object)
# users_id_json = json.dumps(vk_users)
# users_id_object = UsersId.parse_raw(users_id_json)
# print(posts_object.items[0].likes)
print(posts_object.items)

current_date_time = datetime.now() - relativedelta(months=2) - relativedelta(days=datetime.now().day - 1)
format_current_date_time = current_date_time.strftime('%d.%m.%Y')
time_stamp_current_date = time.mktime(datetime.strptime(format_current_date_time, '%d.%m.%Y').timetuple())

print(int(time_stamp_current_date) < posts_object.items[0].date)
post_date = datetime.fromtimestamp(posts_object.items[0].date)

format_post_date = post_date.strftime('%d.%m.%Y')
print(format_post_date)
print(format_current_date_time)
print(current_date_time)

text = """Он собирает залы, обсуждая литературу.
Знает, как запустить успешный творческий проект и сохранить баланс между трудом и отдыхом.

Кто же он?
Выпускник факультета журналистики института общественных наук и массовых коммуникаций НИУ «БелГУ», автор проектов «Белогорье.Science», «Прямая Речь», «Ночная Лига пинг понга», «ВезелкаSup2022», «Гаражка», «БЭУ» и «САМИздат» Дмитрий Ткаченко.

Об истории успеха и планах на будущее в мире литературы – слушайте в нашем подкасте.

#БЕЛыйГусьВещает
#БЕЛыйГУсь"""

item = 'Институт общественных наук и массовых коммуникаций'

regex_text = r''.join([txt[:-3] + '.* ' if len(txt) > 6 else txt + ' ' for txt in item.lower().split()])

print(regex_text)
print(re.search(regex_text, text.lower()))
