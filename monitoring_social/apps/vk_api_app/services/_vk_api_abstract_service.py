from apps.vk_api_app.handlers.redis_handler import RedisHandler
from apps.vk_api_app.handlers.vk_handler import VkHandler
from apps.vk_api_app.handlers.vk_validation_handler import VkValidationHandler


class VkAPIAbstractService:

    def __init__(self, *,
                 redis_handler: RedisHandler,
                 vk_handler: VkHandler,
                 vk_validation: VkValidationHandler):
        self.vk_handler = vk_handler
        self._vk_validation = vk_validation
        self._redis_handler = redis_handler
        self.ids_posts = []

