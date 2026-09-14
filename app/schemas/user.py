from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, examples=["testuser"])
    email: EmailStr = Field(..., examples=["usuario@ejemplo.com"])


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, examples=["securepassword123"])


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None