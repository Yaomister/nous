

from pydantic import BaseModel


class Book(BaseModel):
    title: str
    cover: str
    authors: [str]
    datePublished: str
    model_config = {
        "from_attributes": True
    }
