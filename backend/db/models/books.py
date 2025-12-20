
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
    title: Mapped[str]
    authors: Mapped[list[str]] = mapped_column(JSON)
    cover: Mapped[str]
    datePublished : Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=utcnow())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=utcnow(), server_onupdate=utcnow(), onupdate=utcnow()
    )

