from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from db import models



async def get_or_create_user_index(db: AsyncSession, user_id):
    user = await db.scalar(select(models.UserMLIndex).where(models.UserMLIndex.user_id == user_id))
    if user:
        return user.user_index
    

    next_index = await db.execute(select(func.count()).select_from(models.UserMLIndex)) or 0
    db.add(models.UserMLIndex(user_id = user_id, user_index = next_index))
    await db.commit()
    return next_index

async def get_or_create_book_index(db: AsyncSession, book_id):
    book = await db.scalar(select(models.BookMLIndex).where(models.BookMLIndex.book_id == book_id))

    if (book):
        return book.book_index
    
    next_index = await db.execute(select(func.count()).select_from(models.BookMLIndex)) or 0
    db.add(models.BookMLIndex(book_id = book_id, book_index = next_index))

    await db.commit()
    return next_index