from dataclasses import dataclass
from typing import Self

from apps.monitoring.schemas.team_shemas import TeamSchema
from apps.vk_api_app.models_db.vk_settings import VkSettings
from interfaces.model_to_schemas import IModelToSchema


@dataclass
class VkSettingsSchema(IModelToSchema):
    token: str
    group_id: int
    team: TeamSchema

    @classmethod
    def from_moder(cls, model: VkSettings) -> Self:

        return cls(
            token=model.token,
            group_id=model.group_id,
            team=TeamSchema.from_moder(model=model.team)
        )
