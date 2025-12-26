from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Response, Cookie, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from db import schemas, models
from auth import BadRequestException, NotFoundException
from uuid import UUID
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from utils import load_recommender
from contextlib import asynccontextmanager
from db import models
from utils import recommender
from sqlalchemy import text, select
from auth.jwt import (
    create_token_pair, decode_token_with_blacklisted, refresh_token_state_with_rotation, add_refresh_token_cookie, mail_token, SUB, JTI, EXP, TYP
)




router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.get("/popular")
async def popular(k: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("""
SELECT books.id FROM books JOIN posts ON posts.book_id = books.id GROUP BY books.id ORDER BY COUNT(posts.id) DESC LIMIT :k
"""), {"k" : k})
    
    book_ids = result.scalars().all()

    books = await db.execute(
        select(models.Book).where(models.Book.id.in_(book_ids))
    )

    return books.scalars().all()

@router.get("/trending")
async def trending(k: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("""
SELECT books.id FROM books JOIN posts ON posts.book_id = books.id WHERE posts.created_at >= NOW() - INTERVAL '7 days' GROUP BY books.id ORDER BY COUNT(posts.id) DESC LIMIT :k
"""), {"k" : k})
    
    book_ids = result.scalars().all()

    books = await db.execute(
        select(models.Book).where(models.Book.id.in_(book_ids))
    )

    return books.scalars().all()






@router.get("/recommend")
async def recommend(token: Annotated[str, Depends(oauth2_scheme)], k: int = 10, db: AsyncSession = Depends(get_db)):

    user = await decode_token_with_blacklisted(token, db)

    if not user:
        raise BadRequestException(detail="No user found")
    

    
    user_row = await db.get(models.UserMLIndex, user[SUB]
)

    if not user_row:
        return {"books" : []}
    u = user_row.user_index
    scores = recommender.model.books @ recommender.model.users[u]
    top = scores.argsort()[-k:][::-1].tolist()
    
    rows = await db.execute(
        text(
        "SELECT book_id FROM book_ml_index WHERE book_index = ANY(:idxs)"
        ),
        {"idxs" : top}
    )

    book_ids =  [row[0] for row in rows.fetchall()]

    books = []

    for id in book_ids:
        book = await models.Book.find_by_id(db = db, id =  id)
        if book:
            books.append({
                "title" : book.title,
                "authors" : book.authors,
                "cover" : book.cover,
                "id" : book.id
            })

    return books


