from typing import Any
from fastapi import HTTPException, status
from pydantic import PostgresDsn
import config


from sqlalchemy import select
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase




POSTGRES_URL = PostgresDsn.build(
    scheme="postgresql+asyncpg",
    username=config.POSTGRES_USER,
    password=config.POSTGRES_PASSWORD,
    host=config.POSTGRES_HOST,
    port=int(config.POSTGRES_PORT),
    path=config.POSTGRES_DB,
)




engine = create_async_engine(str(POSTGRES_URL), future=True, echo=True)

SessionFactory = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)

print("API DB:", str(POSTGRES_URL))



class Base(AsyncAttrs, DeclarativeBase):
    async def save(self, db: AsyncSession):
        try:
            db.add(self)
            return await db.commit()

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(e)
            ) from e

    @classmethod
    async def find_by_id(cls, db: AsyncSession, id: str):
        query = select(cls).where(cls.id == id)
        result = await db.execute(query)
        return result.scalars().first()