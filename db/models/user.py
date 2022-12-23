from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel
from db.models.model_base import ModelBase

if TYPE_CHECKING:
    from db.models.messenger import Messenger


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    staff: Optional[int]


class User(UserBase, ModelBase, table=True):
    __tablename__ = "users"

    password: str
    is_blocked: bool = Field(default=False)

    messengers: list["Messenger"] = Relationship(back_populates="owner")


class UserUpdate(SQLModel):
    email: Optional[str]
    staff: Optional[int]
    password: Optional[str]
    is_blocked: Optional[bool]


class UserCreate(UserBase):
    password: str


class UserRead(UserBase, ModelBase):
    is_blocked: bool
