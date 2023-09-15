from dataclasses import dataclass
from datetime import datetime
from typing import Self

from django.contrib.auth.models import User

from interfaces.model_to_schemas import IModelToSchema


@dataclass(frozen=True)
class UserSchema(IModelToSchema):
    username: str
    first_name: str
    last_name: str
    email: str
    is_staff: bool
    is_active: bool
    date_joined: datetime

    @classmethod
    def from_moder(cls, model: User) -> Self | None:

        return cls(
            username=model.username,
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            is_staff=model.is_staff,
            is_active=model.is_active,
            date_joined=model.date_joined
        )

