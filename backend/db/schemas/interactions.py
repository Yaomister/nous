from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional
from enum import Enum


class TargetType(str, Enum):
    book = "book"
    list = "list"


class Post(BaseModel):
    id: UUID4
    created_at: datetime
    book_id : UUID4
    user_id: UUID4
    review : Optional[str]



class Like(BaseModel):
    id: UUID4
    target_type : TargetType
    target_id: UUID4
    created_at: datetime


class Rating(BaseModel):
    id: UUID4
    post_id: Optional[UUID4]
    created_at: datetime
    rating: float