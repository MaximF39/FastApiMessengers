from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from db.models.model_base import ModelBase

if TYPE_CHECKING:
    from . import Messenger
    from .message import Message


class ChatBase(ModelBase):
    chat_id: str  # id in messenger


class Chat(ChatBase, table=True):
    __tablename__ = "chats"

    name: str
    messages: list["Message"] = Relationship(back_populates="chat")
    messenger_id: int = Field(foreign_key="messengers.id")
    messenger: list["Messenger"] = Relationship(back_populates="chats")


class ChatCreate(ChatBase):
    messenger_id: int


class ChatRead(ChatBase):
    name: str
