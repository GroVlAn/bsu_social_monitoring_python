import json
from typing import Optional, List

from pydantic import BaseModel


class CountableValue(BaseModel):
    count: int


class Post(BaseModel):
    id: int
    date: int
    text: str
    likes: Optional[CountableValue] | int
    comments: Optional[CountableValue] | int
    reposts: Optional[CountableValue] | int
    views: Optional[CountableValue] | int
    prefix = 'post-'

    def __str__(self):
        string = '{\n'
        for key in vars(self):
            string += f'\t{key}: {getattr(self, key)}\n'
        else:
            string += '}'
        return string

    def to_json(self):
        return {
            'id': self.id,
            'date': self.date,
            'text': self.text,
            'likes': self.likes.count if self.likes else None,
            "comments": self.comments.count if self.comments else None,
            "reposts": self.reposts.count if self.reposts else None,
            "views": self.views.count if self.views else None
        }


class PostResponse(BaseModel):
    items: List[Post]

    def __str__(self):
        string = '{\n'
        for item in self.items:
            string += f'{item}\n'
        else:
            string += '}'
        return string
