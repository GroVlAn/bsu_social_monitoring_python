from typing import Optional, List

from pydantic import BaseModel


class CountableValue(BaseModel):
    count: int


class Post(BaseModel):
    id: int
    date: int
    text: str
    likes: Optional[CountableValue]
    comments: Optional[CountableValue]
    repost: Optional[CountableValue]
    views: Optional[CountableValue]

    def __str__(self):
        string = '{\n'
        for key in vars(self):
            string += f'\t{key}: {getattr(self, key)}\n'
        else:
            string += '}'
        return string


class PostResponse(BaseModel):
    items: List[Post]

    def __str__(self):
        string = '{\n'
        for item in self.items:
            string += f'{item}\n'
        else:
            string += '}'
        return string
