from pydantic import BaseModel, EmailStr


class UserScheme(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginScheme(BaseModel):
    email: EmailStr
    password: str
