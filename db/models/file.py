from sqlmodel import Relationship

from db.models.message import Message
from db.models.schemas import FileBase


class File(FileBase, table=True):
    __tablename__ = "files"

    message: Message = Relationship(back_populates="files")

# class FileWithMessage(FileBase):
#     message: MessageRead
