from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from db import schemas, models
from auth import BadRequestException, NotFoundException
from uuid import UUID
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from auth.jwt import (
    create_token_pair, decode_token_with_blacklisted, refresh_token_state_with_rotation, add_refresh_token_cookie, mail_token, SUB, JTI, EXP, TYP
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


router = APIRouter()



@router.get("/details/{id}")
async def get_book_details(id: UUID, db = Depends(get_db)):
    book_details = await models.Book.find_by_id(id=id, db=db)
    if not book_details:
        raise NotFoundException(detail="Book not found")
    
    return schemas.Book.model_validate(book_details)



@router.post("/post")
async def create_post(token: Annotated[str , Depends(oauth2_scheme)], data: schemas.CreatePost, db= Depends(get_db)):

    payload = await decode_token_with_blacklisted(token=token, db=db)
    user = await models.User.find_by_id(db = db, id = payload[SUB])
    if not user:
        raise NotFoundException(details="User not found")
    

    book = await models.Book.find_by_id(db = db, id=data.book_id)
    if not book:
        raise NotFoundException(detail="Book not found")
    
    post = models.Post(user_id = user.id, book_id = book.id, review = data.review, would_recommend = data.would_recommend, read_before = data.read_before)


    await post.save(db = db)

    if (data.rating is not None):
        rating = models.Rating(post_id = post.id, rating = data.rating)

        await rating.save(db = db)


    if (data.like is not None):
        # check if already liked, then do corresponding action
        already_exists = await models.Like.find_by_user_id_and_target_id(db = db, user_id=user.id, target_id=book.id)
        if(not already_exists and data.like == True):
            like = models.Like(target_id = book.id, target_type = "book", user_id = user.id)
            await like.save(db = db)
        elif(already_exists and data.like == False):
            await db.delete(already_exists)
        

    await db.commit()

    return post


    

