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


router = APIRouter()



@router.get("/recommend/{user_id}")
async def recommend(user_id, k: int = 10, db: AsyncSession = Depends(get_db)):
    user_row = await db.get(models.UserMLIndex, user_id)
    if not user_row:
        return {"books" : []}
    u = user_row.user_index
    scores = recommender.model.books @ recommender.model.users[u]
    top = scores.argsort()[-k:][::-1]

    rows = await db.execute(
        "SELECT book_id FROM book_ml_index WHERE book_index = ANY(:idxs)",
        {"idxs" : top.tolist()}
    )

    return {"books" : [r[0] for r in rows.fetchall()]}


