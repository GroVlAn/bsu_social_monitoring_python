from typing import List

from pydantic import BaseModel


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
