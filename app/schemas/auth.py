import strawberry
from .user import UserType

@strawberry.input
class LoginInput:
    email: str
    password: str

@strawberry.type
class LoginResponse:
    token: str
    user: UserType
