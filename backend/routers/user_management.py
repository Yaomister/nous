from typing import Annotated
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Response, Cookie
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from db import SuccessResponseSchema, schemas
from db.models import User


from pydantic import ValidationError

from db import get_db
from db import User
from config import REFRESH_TOKEN_ROTATION
from auth import get_password_hash
from auth.jwt import (
    create_token_pair, decode_token_with_blacklisted, refresh_token_state_with_rotation, add_refresh_token_cookie, mail_token, SUB, JTI, EXP
)

import logging
logger = logging.getLogger("validators")

from auth import BadRequestException, NotFoundException, AuthFailedException, ForbiddenException


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register", response_model=schemas.User, status_code=201)
async def register(
    data: schemas.UserRegister,
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
   
   user_schema = schemas.User.from_orm(user)

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
    


# @router.post("refresh")
# async def refresh(
#     response: Response,
#     refresh: Annotated[str | None, Cookie()] = None,
#     db: AsyncSession = Depends(get_db)
# ):
#     if not refresh:
#         raise BadRequestException("Refresh token required")
    

#     if not REFRESH_TOKEN_ROTATION:return refresh_token_state_without_rotation(token=refresh)

#     payload = await decode_token_with_blacklisted(token=refresh)
#     user = await userSchemas.USer.find_by_id(db=db, id=payload[SUB])

#     return await refresh_token_state_with_rotation(
#         response=response,
#         payload=payload,
#         user=user,
#         db=db
#     )


# @router.get("/verify", response_model=userSchemas.SuccessResponseSchema)
# async def verify(token: str, db: AsyncSession = Depends(get_db)):
#     payload = await decode_token_with_blacklisted(token = token, db=db)
#     user = await userSchemas.User.find_by_id(db=db, id=payload[SUB])
#     if not user:
#         raise NotFoundException(detail="User not found")
    
#     user.is_active = True
#     await user.save(db=db)
#     return {"msg": "Successfully activated"}

# @router.post("/logout", response_model= userSchemas.SuccessResponseSchema)
# async def logout(
#     token: Annotated[str, Depends(oauth2_scheme)],
#     db: AsyncSession= Depends(get_db)
# ):
    
#     payload = await decode_token_with_blacklisted(token=token, db=db)
#     black_listed= userSchemas.BlackListToken(
#         id=payload[JTI], expire=datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
#     )

#     await black_listed.save(db=db)

#     return {"msg" : "Successfully logout"}

# @router.post("/forgot-password", response_model=userSchemas.SuccessResponseSchema)
# async def forgot_password(
#     data: userSchemas.ForgotPasswordSchema,
#     bg_task: BackgroundTasks,
#     db: AsyncSession = Depends(get_db),
# ):
#     # user = await models.User.find_by_email(db=db, email = data.email)
#     # if user:
#     #     user_schema = schemas.User.from_orm(user)
#     #     reset_token=mail_token(user_schema)
#     #     mail_task_data = schemas.MailTaskSchema(
#     #         user=user_schema,
#     #         body=schemas.MailBodySchema(type="password-reset", token=reset_token)
#     #     )
#     #   bg_task.add_task(user_mail_event, mail_task_data)

#     return {"msg" : "Reset token sended successfully to your email"}

# @router.post("/password-reset", response_model=userSchemas.SuccessResponseSchema)
# async def password_reset_token(
#     token: str,
#     data: userSchemas.PasswordResetSchema,
#     db: AsyncSession = Depends(get_db),
# ):
#     payload = await decode_token_with_blacklisted(token=token,db=db)
#     user = await userSchemas.User.find_by_id(db=db, id=payload[SUB])
#     if not user:
#         raise NotFoundException(detail="UserNotFound")
    
#     user.password = get_password_hash(data.password)
#     await user.save(db=db)

#     return {"msg": "Password successfully updated"}

# @router.post("/password-update", response_model=userSchemas.SuccessResponseSchema)
# async def password_update(
#     token: Annotated[str, Depends(oauth2_scheme)],
#     data: userSchemas.PasswordUpdateSchema,
#     db: AsyncSession = Depends(get_db),
# ):
#     payload = await decode_token_with_blacklisted(token = token, db=db)
#     user = await userSchemas.User.find_by_id(db=db, id=payload[SUB])
#     if not user:
#         raise NotFoundException(detail="User no found")
    
#     if not verify(data.old_password, user.password):
#         try: 
#             user.OldPasswordErrorSchema(old_passsword=False)
#         except ValidationError as e:
#             raise RequestValidationError(e.raw_errors)
#     user.password = get_password_hash(data.password)
#     await user.save(db=db)

#     return {"msg" : "Successfully updated"}


# @router.get("/books")
# async def articles(
#     token: Annotated[str, Depends(oauth2_scheme)],
#     db: AsyncSession = Depends(get_db),
# ):
#     payload = await decode_token_with_blacklisted(token=token, db=db)
#     user = await decode_token_with_blacklisted(token=token, db=db)
#     if not user:
#         raise NotFoundException(detail="User not found")
    
#     # Get the books


    


