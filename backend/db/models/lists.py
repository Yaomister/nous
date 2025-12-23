from db import Base
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class List(Base):
    __tablename__ = "lists"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    list_entries = relationship("ListEntry", back_populates="list", cascade="all, delete orphan")
    title: Mapped[str]

class ListEntry(Base):
    __tablename__ = "list_entries"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    list_id  = mapped_column(ForeignKey("lists.id"), nullable=False)
    book_id = mapped_column(ForeignKey("books.id"), nullable=False)
    list = relationship("List", back_populates="list_entries")
    