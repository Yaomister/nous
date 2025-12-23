from db import Base
from auth.utils import utcnow
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
import uuid
from enum import Enum
from sqlalchemy import Enum as SQLEnum



class TargetType(str, Enum):
    book = "book"
    list = "list"



class Post(Base):
    __tablename__ = "posts"
    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    created_at : Mapped[datetime] = mapped_column(default=utcnow)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("User")
    review: Mapped[str] = mapped_column(default="")

class Like(Base):
    __tablename__ = "likes"
    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4,primary_key=True)
    created_at: Mapped[datetime]= mapped_column(default=utcnow)
    target_type: Mapped[TargetType] = mapped_column(SQLEnum(TargetType), nullable=False)
    target_id: Mapped[uuid.UUID]


class Rating(Base):
    __tablename__ = "ratings"
    id : Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    post_id = mapped_column(ForeignKey("posts.id"), nullable=False)
    post = relationship("Post")
    created_at: Mapped[datetime]= mapped_column(default=utcnow)
    rating: Mapped[float]

