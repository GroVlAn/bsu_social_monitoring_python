from django.db import models
from vk_api_app.models_db.vk_post import *
from vk_api_app.models_db.vk_settings import *
from vk_api_app.models_db.vk_user import *


__all__ = [
    'VkPost',
    'VkSettings',
    'VkUserStatistic',
    'VkUser'
]
