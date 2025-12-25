from db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import select, ForeignKey, Text

from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime
import uuid
from enum import Enum
from sqlalchemy import Enum as SQLEnum
from auth.utils import utcnow




class TargetType(str, Enum):
    book = "book"
    list = "list"



class Post(Base):
    __tablename__ = "posts"
    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    created_at : Mapped[datetime] = mapped_column(server_default=utcnow())
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("User")
    book_id = mapped_column(ForeignKey("books.id"), nullable=False)
    book = relationship("Book")
    review: Mapped[str] = mapped_column(default="")
    would_recommend: Mapped[bool]
    read_before: Mapped[bool]

class Like(Base):
    __tablename__ = "likes"
    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4,primary_key=True)
    created_at: Mapped[datetime]= mapped_column(server_default=utcnow())
    target_type: Mapped[TargetType] = mapped_column(SQLEnum(TargetType), nullable=False)
    target_id: Mapped[uuid.UUID]
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("User")

    @classmethod 
    async def find_by_user_id_and_target_id(cls, db: AsyncSession, user_id: uuid.UUID, target_id : uuid.UUID):
        query = select(cls).where(cls.user_id == user_id, cls.target_id == target_id)
        result = await db.execute(query)
        return result.scalars().first()



class Rating(Base):
    __tablename__ = "ratings"
    id : Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    post_id = mapped_column(ForeignKey("posts.id"), nullable=False)
    post = relationship("Post")
    created_at: Mapped[datetime]= mapped_column(server_default=utcnow())
    rating: Mapped[float]

