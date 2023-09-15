from dataclasses import dataclass
from datetime import datetime
from typing import Self

from apps.monitoring.schemas.search_items_schemas import SearchItemSchema
from apps.vk_api_app.models_db.vk_post import VkPost
from interfaces.model_to_schemas import IModelToSchema


@dataclass
class VkPostSchema(IModelToSchema):
    id_post: int
    text: str
    date: datetime
    likes: int
    comments: int
    reposts: int
    views: int
    search_item: SearchItemSchema

    @classmethod
    def from_moder(cls, model: VkPost) -> Self:

        return cls(
            id_post=model.id_post,
            text=model.text,
            date=model.date,
            likes=model.likes,
            comments=model.comments,
            reposts=model.reposts,
            views=model.views,
            search_item=SearchItemSchema.from_moder(model=model.search_item)
        )
