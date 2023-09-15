from dataclasses import dataclass
from datetime import datetime
from typing import Self

from apps.monitoring.models_db.statistics import Statistics
from apps.monitoring.schemas.search_items_schemas import SearchItemSchema
from interfaces.model_to_schemas import IModelToSchema


@dataclass(frozen=True)
class StatisticsSchema(IModelToSchema):
    likes: str
    comments: str
    reports: str
    date_from: datetime
    date_to: datetime
    owner: SearchItemSchema

    @classmethod
    def from_moder(cls, model: Statistics) -> Self:

        return cls(
            likes=model.likes,
            comments=model.comments,
            reports=model.reposts,
            date_from=model.date_from,
            date_to=model.date_to,
            owner=SearchItemSchema.from_moder(model=model.owner)
        )
