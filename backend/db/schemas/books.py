

from pydantic import BaseModel
from typing import Optional


class Book(BaseModel):
    title: str
    cover: str
    authors: list[str]
    datePublished: str
    isbn: Optional[str] = None
    release_date: Optional[str] = None
    language: Optional[str] = None
    pages: Optional[int] = None
    description: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
