from pydantic import BaseModel, UUID4
from typing import Optional


class List(BaseModel):
    id: UUID4
    title: str
    list_entries: list[UUID4]
    user_id: UUID4


class ListEntry(BaseModel):
    id: UUID4
    book_id: UUID4
    list_Id: UUID4
