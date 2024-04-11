from pydantic import BaseModel
from typing import Optional

"""Module for database models"""


class User(BaseModel):
    """User model

    Fields:
        id: int
        email: str
        group_id: int
    """

    id: int
    email: str
    group_id: int


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


class Group(BaseModel):
    """Group model

    Fields:
        id: int
        api_id: int
    """

    id: int
    api_id: int
