from pydantic import BaseModel, UUID4, field_validator
from datetime import datetime
from typing import Optional
from enum import Enum


class TargetType(str, Enum):
    book = "book"
    list = "list"


class Post(BaseModel):
    id: UUID4
    book_id : UUID4
    user_id: UUID4
    review : Optional[str]

class CreatePost(BaseModel):
    book_id: UUID4
    review: Optional[str]
    like: bool
    rating: Optional[float]
    read_before: bool
    would_recommend:bool


class Like(BaseModel):
    id: UUID4
    target_type : TargetType
    target_id: UUID4
    user_id: UUID4
    read_before: bool
    would_recommend: bool

class CreateLike(BaseModel):
    target_type: TargetType
    target_id: str

    @field_validator("target_type")
    @classmethod
    def validate_target_type(cls, value, values, **kwargs):
        if not value or value not in TargetType.__members__:
            return None
        return value


class Rating(BaseModel):
    id: UUID4
    post_id: UUID4
    rating: float


    class CreateRating(BaseModel):
        post_id: UUID4
        rating:float
