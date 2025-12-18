import uuid
import sys
from datetime import timedelta, datetime, timezone

from jose import jwt, JWTError
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

import config
from db import User
from db import TokenPair, JwtTokenSchema
from .exceptions import AuthFailedException
from db import BlackListToken, User as DBUser

REFRESH_COOKIE_NAME = "refresh"
SUB = "sub"
EXP = "exp"
IAT = "iat"
JTI = "jti"


def get_utc_now():
    return datetime.now(timezone.utc)


def create_access_token( payload: dict, minutes: int| None = None) -> JwtTokenSchema:
    expire = get_utc_now() + timedelta(minutes= minutes or config.ACCESS_TOKEN_EXPIRES_MINUTES)

    payload[EXP] = expire

    token = JwtTokenSchema(
        token=jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM),
        expire = expire,
        payload = payload
    )

    return token


def create_refresh_token(payload: dict, minutes: int | None = None) -> JwtTokenSchema:
    expire = get_utc_now() + timedelta(minutes=minutes or config.REFRESH_TOKEN_ROTATION_MINUTES)

    payload[EXP] = expire

    token = JwtTokenSchema(
        token=jwt.encode(payload, config.JWT_SECRET_KEY, algorithm=config.ALGORITHM),
        expire = expire,
        payload=payload
    )
    return token


def create_token_pair(user : User) -> TokenPair:
    payload = {SUB: str(user.id), JTI : str(uuid.uuid4()), IAT: get_utc_now()}

    return TokenPair(
        access=create_access_token(payload={**payload}),
        refresh=create_access_token(payload={**payload})
    )


async def decode_token_with_blacklisted(token: str, db: AsyncSession):
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.ALGORITHM])
        blacklist_token = await BlackListToken.find_by_id(db, payload.get(JTI))
        if (blacklist_token):
            raise JWTError("Token has been blacklisted")
        
    except JWTError:
        raise AuthFailedException()
    
    return payload

async def refresh_token_state_with_rotation(response: Response, payload: dict, user : DBUser, db: AsyncSession):
    exp = datetime.fromtimestamp(payload.get(EXP))
    exp = exp.replace(tzinfo=timezone.utc)
    black_listed = BlackListToken(
        id=payload[JTI], expire=exp
    )
    await black_listed.save(db =db)
    token_pair = create_token_pair(user=user)

    add_refresh_token_cookie(response=response, token = token_pair.refresh.token)

    return {"token" : token_pair.access.token}



async def refresh_token_state_without_rotation(token: str):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])

    except JWTError:
        raise AuthFailedException()
    
    return {"token" : create_access_token(payload=payload).token}



def mail_token(user: User):
    payload = {SUB: str(user.id), JTI: str(uuid.uuid4()), IAT : get_utc_now()}
    return create_access_token(payload=payload, minutes=2 * 60).token


def add_refresh_token_cookie(response: Response, token: str):
    exp = get_utc_now() + timedelta(minutes=config.REFRESH_TOKEN_EXPIRES_MINUTES)
    exp.replace(tzinfo=timezone.utc)
    response.set_cookie(
        key= REFRESH_COOKIE_NAME,
        value=token,
        expires=int(exp.timestamp()),
        httponly=True,
    )