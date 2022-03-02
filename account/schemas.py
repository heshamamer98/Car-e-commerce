from typing import Optional

from ninja import Schema
from pydantic import EmailStr, Field


class AccountCreate(Schema):
    first_name: str
    last_name: str
    email: EmailStr
    password1: str = Field(min_length=8)
    password2: str


class AccountOut(Schema):
    first_name: str
    last_name: str
    email: EmailStr


class TokenOut(Schema):
    access: str

class AuthOut(Schema):
    token: TokenOut
    account: AccountOut

class SigninSchema(Schema):
    email: EmailStr
    password: str


class AccountUpdate(Schema):
    first_name: str
    last_name: str
    


class ChangePasswordSchema(Schema):
    old_password: str
    new_password1: str
    new_password2: str