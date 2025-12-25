import uuid
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
from sqlalchemy import Integer


class UserMLIndex(Base):
    __tablename__ = "user_ml_index"
    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, nullable=False)
    user_index: Mapped[int] = mapped_column(Integer, nullable=False, unique=True) 


class BookMLIndex(Base):
    __tablename__ = "book_ml_index"
    book_id : Mapped[uuid.UUID] = mapped_column(primary_key=True, nullable=False)
    book_index : Mapped[int] = mapped_column(Integer, nullable=False, unique=True)


