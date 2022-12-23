from datetime import datetime

from sqlmodel import Field

from db.models.model_base import ModelBase


class FileBase(ModelBase):
    path: str
    sent_at: datetime
    message_id: int = Field(foreign_key="messages.id")


class FileRead(FileBase):
    pass
