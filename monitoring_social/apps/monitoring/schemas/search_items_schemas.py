from dataclasses import dataclass
from datetime import datetime
from typing import Self, Optional

from apps.monitoring.models_db.search_items import GroupSearchItems, SearchItem, SearchItemsSummaryStatistics
from apps.monitoring.schemas.team_shemas import TeamSchema
from interfaces.model_to_schemas import IModelToSchema


@dataclass(frozen=True)
class GroupSearchItemsSchema(IModelToSchema):
    name: str
    ru_name: str
    level: int
    team: TeamSchema

    @classmethod
    def from_moder(cls, model: GroupSearchItems) -> Self:

        return cls(
            name=model.name,
            ru_name=model.ru_name,
            level=model.level,
            team=TeamSchema.from_moder(model=model.team)
        )


@dataclass(frozen=True)
class SearchItemSchema(IModelToSchema):
    name: str
    description: str
    time_create: datetime
    time_update: datetime
    team: TeamSchema
    group: GroupSearchItemsSchema
    parent: Optional[Self]

    @classmethod
    def from_moder(cls, model: SearchItem) -> Self:

        return cls(
            name=model.name,
            description=model.description,
            time_create=model.time_create,
            time_update=model.time_update,
            team=TeamSchema.from_moder(model=model.team),
            group=GroupSearchItemsSchema.from_moder(model=model.group),
            parent=cls.from_moder(model=model.parent) if model.parent else None
        )


@dataclass(frozen=True)
class SearchItemsSummaryStatisticsSchema(IModelToSchema):
    owner: SearchItemSchema
    likes: str
    comments: str
    reports: str
    score: int

    @classmethod
    def from_moder(cls, model: SearchItemsSummaryStatistics) -> Self:

        return cls(
            owner=SearchItemSchema.from_moder(model=model.owner),
            likes=model.likes,
            comments=model.comments,
            reports=model.reposts,
            score=model.score
        )
