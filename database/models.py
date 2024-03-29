from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str


class Cookie(BaseModel):
    name: str
    value: str
    domain: Optional[str] = None
    path: Optional[str] = None
    expiry: Optional[int] = None
    httpOnly: Optional[bool] = None
    secure: Optional[bool] = None
