from pydantic import BaseModel
from typing import Optional

"""Module for database models"""


class User(BaseModel):
    """User model

    Fields:
        id: int
        email: str
    """

    id: int
    email: str


class Cookie(BaseModel):
    """Cookie model

    Fields:
        name: str
        value: str
        domain: Optional[str] = None
        path: Optional[str] = None
        expiry: Optional[int] = None
        httpOnly: Optional[bool] = None
        secure: Optional[bool] = None
    """

    name: str
    value: str
    domain: Optional[str] = None
    path: Optional[str] = None
    expiry: Optional[int] = None
    httpOnly: Optional[bool] = None
    secure: Optional[bool] = None
