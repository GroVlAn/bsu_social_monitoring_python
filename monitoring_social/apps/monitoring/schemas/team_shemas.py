from dataclasses import dataclass
from datetime import datetime
from typing import Self, Tuple, Any

from apps.authentication.schemas.user_schemas import UserSchema
from apps.monitoring.models_db.team import Team
from interfaces.model_to_schemas import IModelToSchema


@dataclass(frozen=True)
class TeamSchema(IModelToSchema):
    name: str
    slug: str
    description: str
    time_create: datetime
    time_update: datetime
    user: Tuple[UserSchema | None]

    @classmethod
    def from_moder(cls, model: Team) -> Self:

        return cls(
            name=model.name,
            slug=model.slug,
            description=model.description,
            time_create=model.time_create,
            time_update=model.time_update,
            user=tuple(UserSchema.from_moder(model=user) for user in model.users.all())
        )

