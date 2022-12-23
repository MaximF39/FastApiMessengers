from typing import Optional

from sqlmodel import SQLModel

from db.models import Messenger
from db.models.chat import ChatRead
from db.models.messenger import MessengerCreate, MessengerUpdate, MessengerRead


class Whatsapp(Messenger):

    @property
    def profile_id(self):
        return self.secret_dict["profile_id"]

    @property
    def token(self):
        return self.secret_dict["token"]

    def chats(self) -> ChatRead:
        for dialog in self.client.iter_dialogs():
            yield ChatRead(name=dialog.name,
                           chat_id=dialog.id)


class WhatsappRead(MessengerRead):
    pass


class WhatsappSecret(SQLModel):
    token: str
    profile_id: str


class WhatsappCreate(MessengerCreate):
    secret: WhatsappSecret


class WhatsappUpdate(MessengerUpdate):
    secret: Optional[WhatsappSecret]
