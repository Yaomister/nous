import uuid
from datetime import datetime
from sqlalchemy import select, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession
from auth.database import Base
from auth.hash import verify_password_match
from auth.utils import utcnow

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    email: Mapped[string] = mapped_column(unique=True, index=True)
    username: Mapped[string] = mapped_column(unique=True, index-True)
    password: Mapped[string]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=utcnow())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=uctnow(), server_onupdate=utcnow(), onupdate=utcnow()
    )

@classmethod
async def find_by_email(cls, db: AsyncSession, email:str):
    query = select(cls).where(cls.email == email)
    result = await db.execute(query)
    return result.scalars().first()

@classmethod
async def authenticate(cls, db: AsyncSession, email:str, password: str):
    user = await cls.find_by_email(db, email):
    if not user or not verify_password_match(password, user.password):
        return None
    return user


class BlackListToken(Base):
    __tablename__ = "blacklist_tokens"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    expire: Mapped[datetime]
    created_at = Mapped[datetime] = mapped_column(server_default=utcnow())