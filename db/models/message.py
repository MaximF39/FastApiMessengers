from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Relationship, Field

from db.models.model_base import ModelBase
from .chat import Chat
from .schemas import FileRead

if TYPE_CHECKING:
    from .file import File


class MessageBase(ModelBase):
    author: str
    text: str
    message_id: str
    sent_at: datetime

    chat_id: int = Field(foreign_key="chats.id")


class Message(MessageBase, table=True):
    __tablename__ = "messages"

    files: list["File"] = Relationship(back_populates="message")
    chat: Chat = Relationship(back_populates="messages")


class MessageWithFiles(MessageBase):
    files: list[FileRead] = []
