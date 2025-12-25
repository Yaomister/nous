
from typing import Any
from datetime import datetime
from pydantic import BaseModel, UUID4, field_validator, EmailStr
import re


class UserBase(BaseModel):
    email: EmailStr
    username: str
    model_config = {
        "from_attributes": True
    }


class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID4

    class Config:
        orm_mode = True

    @field_validator("id")
    def convert_to_str(cls, v, values,**kwargs):
        return str(v) if v else v

class UserRegister(UserBase):
    username: str
    email:str
    password: str

    @field_validator("email")
    @classmethod
    def verify_email(cls, value, **kwargs):
        if not value or not re.search(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}", value, re.IGNORECASE) or " " in value:
            raise ValueError("Invalid email")
        return value


    @field_validator("username")
    @classmethod
    def verify_username(cls, value, **kwargs):
        if not value or not re.fullmatch(r"^[A-Za-z0-9_]+$", value) or len(value) > 20:
            print(value)
            raise ValueError("Invalid username")
        return value

    @field_validator("password")
    @classmethod
    def verify_password_match(cls, value, **kwargs):
        print(value)
        if not value or (len(value) < 8) or not re.search(r"[`!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?~]", value):
            print(value)
            raise ValueError("Invalid password")
        return value
    

    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class JwtTokenSchema(BaseModel):
    token: str
    payload: dict
    expire: datetime

class TokenPair(BaseModel):
    access: JwtTokenSchema
    refresh: JwtTokenSchema

class RefreshToken(BaseModel):
    refresh: str

class SuccessResponseSchema(BaseModel):
    msg: str

class BlackListToken(BaseModel):
    id: UUID4
    expire: datetime
    class Config: 
        orm_mode: bool


class ForgotPasswordSchema(BaseModel):
    email: EmailStr


class PasswordResetSchema(BaseModel):
    password: str
    confirm_password: str
    

@field_validator("confirm_password")
def verify_password_match(cls, value, values, **kwargs):
    password = values.get("password")

    if (value != password):
        raise ValueError("The two passwords did not match.")

    return value

class PasswordUpdateSchema(PasswordResetSchema):
    old_password: str

class OldPasswordErrorSchema(BaseModel):
    old_password: bool

@field_validator("old_password")
def check_old_password_status(cls, value, values, **kwargs):
    if not value:
        raise ValueError("Old password is not correct")
