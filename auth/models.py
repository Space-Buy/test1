from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str
    password: str
    is_employee: bool=False
    is_staff: bool=False
class Login(BaseModel):
	username: str
	password: str
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: Optional[str] = None


class TodoModel(BaseModel):
    name: str
    age: int