from enum import IntEnum, auto
from typing import Optional

from sqlmodel import SQLModel, Field


class TypeMessenger(SQLModel, table=True):
    __tablename__ = "types_messenger"

    id: Optional[int] = Field(primary_key=True)
    name: str = Field(unique=True)


class EnumTypeMessenger(IntEnum):
    telegram: int = auto()
    whatsapp: int = auto()


def type_messenger_migrate(session):
    for name, id in EnumTypeMessenger._member_map_.items():
        messenger = TypeMessenger(id=id, name=name)
        session.add(messenger)
    session.commit()
