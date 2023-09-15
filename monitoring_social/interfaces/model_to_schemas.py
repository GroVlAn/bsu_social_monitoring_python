from typing import Self

from django.db.models import Model
from abc import ABC, abstractmethod


class IModelToSchema(ABC):

    @classmethod
    @abstractmethod
    def from_moder(cls, model: Model) -> Self:
        pass
