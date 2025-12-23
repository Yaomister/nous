
import uuid
from db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from auth.utils import utcnow
from sqlalchemy import JSON



class Book(Base):
    __tablename__ = "books"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    isbn: Mapped[str] = mapped_column(nullable=True)
    release_date: Mapped[str] = mapped_column(nullable=True)
    language: Mapped[str] = mapped_column(nullable=True)
    pages: Mapped[int] = mapped_column(nullable=True)
    title: Mapped[str] = mapped_column(nullable=False)
    authors: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    cover: Mapped[str] 
    datePublished : Mapped[str]
    description : Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=utcnow())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=utcnow(), server_onupdate=utcnow(), onupdate=utcnow()
    )

