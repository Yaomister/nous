

from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import MappedColumn, mapped_column
from pydantic import UUID4

class Book(BaseModel):
    id : UUID4
    title: str = mapped_column(nullable=False)
    cover: str
    authors: list[str] = mapped_column(nullable=False)
    datePublished: str
    isbn: Optional[str] = None
    release_date: Optional[str] = None
    language: Optional[str] = None
    pages: Optional[int] = None
    description: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
