import strawberry
from typing import Optional
from datetime import datetime

@strawberry.type
class UserType:
    id: int
    name: str
    email: str
    avatar_url: Optional[str] = None
    avatar_thumbnail_url: Optional[str] = None

@strawberry.input
class UserInput:
    name: str
    email: str
    password: str

@strawberry.input
class UserUpdateInput:
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
