import json
from typing import Optional, TYPE_CHECKING

from fastapi import HTTPException, status
from sqlmodel import Field, Relationship, SQLModel

from db.models import ModelBase

if TYPE_CHECKING:
    from db.models.chat import Chat
    from . import User


class Messenger(ModelBase, table=True):
    __tablename__ = "messengers"
    owner_id: int = Field(foreign_key="users.id")
    owner: "User" = Relationship(back_populates="messengers")
    is_active: bool = Field(default=False)
    chats: list["Chat"] = Relationship(back_populates="messenger")
    phone: Optional[str] = Field(index=True)
    secret: str
    type_id: int = Field(foreign_key="types_messenger.id")

    @property
    def secret_dict(self) -> dict:
        return json.loads(self.secret)

    def check_active(self):
        if not self.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Please activate your account")

    def factory(self):
        from logic.telegram import Telegram
        from logic.whatsapp import Whatsapp
        from .type_messenger import EnumTypeMessenger
        match self.type_id:
            case EnumTypeMessenger.telegram:
                return Telegram
            case EnumTypeMessenger.whatsapp:
                return Whatsapp


class MessengerRead(ModelBase):
    owner_id: int
    type_id: int
    is_active: int
    phone: str


class MessengerCreate(SQLModel):
    phone: str
    owner_id: int


class MessengerUpdate(SQLModel):
    owner_id: Optional[int]
    is_active: Optional[bool]
    phone: Optional[str]
