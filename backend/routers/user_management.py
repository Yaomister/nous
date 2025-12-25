from typing import Annotated
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Response, Cookie
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from db import SuccessResponseSchema, ForgotPasswordSchema, schemas
from db.models import User
from mail import send_reset_email


from pydantic import ValidationError

from db import get_db
from db import User
from config import REFRESH_TOKEN_ROTATION
from auth import get_password_hash
from auth.jwt import (
    create_token_pair, decode_token_with_blacklisted, refresh_token_state_with_rotation, refresh_token_state_without_rotation,  add_refresh_token_cookie, mail_token, SUB, JTI, EXP, TYP
)



import logging
logger = logging.getLogger("validators")

from auth import BadRequestException, NotFoundException, AuthFailedException, ForbiddenException


router = APIRouter()


@router.post("/register", response_model=schemas.User, status_code=201)
async def register(
    data: schemas.UserRegister,
    bg_task: BackgroundTasks,
    db: AsyncSession =  Depends(get_db)
):

   user =  await User.find_by_email(db=db, email=data.email)

   if (user):
       print(user.username)
       raise HTTPException(404, detail="Email already registered")
   
   
   user_data = data.model_dump()
   user_data["password"] = get_password_hash(data.password)   


   user = User(**user_data)
   await user.save(db = db)
   
   user_schema = schemas.User.model_validate(user)

   verify_token = mail_token(user_schema)

   bg_task.add_task(send_reset_email, data.email, "www.google.com")


   return user_schema
    


@router.post("/login")
async def login(
    data: schemas.UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    user = await User.authenticate(db=db, email=data.email, password=data.password)
    if not user:
        raise BadRequestException("Incorrect password or email")
    
    if not user.is_active:
        raise ForbiddenException("Inactive user")
    
    user = schemas.User.model_validate(user)

    token_Pair = create_token_pair(user = user)

    add_refresh_token_cookie(response=response, token=token_Pair.refresh.token)

    return {"token" : token_Pair.access.token}
    


@router.post("/reset-password-link")
async def send_reset_password_link(
    data: ForgotPasswordSchema,
    bg_task: BackgroundTasks, 
    db: AsyncSession = Depends(get_db)
):
    user = await User.find_by_email(db = db, email=data.email)
    if user:
        user_schema = schemas.User.model_validate(user)
        reset_token = mail_token(user_schema, "reset password")
       
       
        bg_task.add_task(send_reset_email, data.email, f"http://localhost:5173/reset-password/{reset_token}")
        
        return {"msg" : "Reset token sended successfully to your email"}
    else:
        raise BadRequestException("Email not registered")


@router.post("/reset-password", response_model=schemas.SuccessResponseSchema)
async def reset_password(
    token: str,
    data: schemas.PasswordResetSchema,
    db: AsyncSession = Depends(get_db)
):
    payload = await decode_token_with_blacklisted(token=token, db=db)
    user = await User.find_by_id(db=db, id = payload[SUB])
    if not user:
        raise NotFoundException(detail="User not found")
    print(payload[TYP])
    if payload[TYP] != "reset password":
        raise BadRequestException(detail="Invalid reset token")
    
    user.password = get_password_hash(data.password)
    await user.save(db=db)

    return {"msg" : "Password successfully updated"}

@router.post("/refresh")
async def refresh(
    response: Response,
    refresh: Annotated[str | None, Cookie()] = None,
    db: AsyncSession = Depends(get_db)
):

    if not refresh:
        raise BadRequestException(detail="Request token required")
    
    if not REFRESH_TOKEN_ROTATION:
        return refresh_token_state_without_rotation(token = refresh)
    
    payload = await decode_token_with_blacklisted(token=refresh, db=db)
    
    user = await User.find_by_id(db=db, id = payload[SUB])

    return await refresh_token_state_with_rotation(response=response, payload=payload, user=user, db=db)